import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, State, ctx
import plotly.graph_objs as go
from datetime import timedelta
import neurokit2 as nk
from tqdm import tqdm
import os

def prepare_signal_segment(df, start_idx, signal_col, clean_func,
                           segment_duration_sec, sampling_rate, max_delta_sec, clean_padding_ratio):
    """
    Prepare a signal segment for quality assessment with appropriate padding.
    
    Extracts a segment from the dataframe, applies cleaning with padding to avoid edge effects,
    and returns both raw and cleaned versions along with corresponding timestamps.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing signal data with a 'time' column
    start_idx : int
        Starting index for the segment
    signal_col : str
        Column name containing the signal data
    clean_func : callable
        Function to clean the signal (e.g., nk.ppg_clean)
    segment_duration_sec : float
        Duration of each segment in seconds
    sampling_rate : int
        Sampling rate of the signal in Hz
    max_delta_sec : float
        Maximum time shift for autocorrelation analysis
    clean_padding_ratio : float
        Ratio of segment length to use for padding during cleaning
    
    Returns
    -------
    tuple
        (signal_raw_trimmed, signal_cleaned_core, signal_cleaned_extended, time)
        - signal_raw_trimmed: Raw signal for the core segment
        - signal_cleaned_core: Cleaned signal for the core segment
        - signal_cleaned_extended: Cleaned signal with additional padding for autocorrelation
        - time: List of timestamps for the core segment
    """

    segment_length = segment_duration_sec * sampling_rate
    clean_padding = int(clean_padding_ratio * segment_length)
    delta_padding = int(max_delta_sec * sampling_rate)

    total_padding_before = clean_padding
    total_padding_after = clean_padding + delta_padding

    start = max(0, start_idx - total_padding_before)
    end = start_idx + segment_length + total_padding_after
    segment_df = df.iloc[start:end]
    signal_raw = segment_df[signal_col].values

    signal_cleaned_full = clean_func(signal_raw, sampling_rate=sampling_rate)
    plot_start = total_padding_before
    plot_end = plot_start + segment_length

    signal_cleaned_core = signal_cleaned_full[plot_start:plot_end]
    signal_cleaned_extended = signal_cleaned_full[plot_start:plot_end + delta_padding]
    signal_raw_trimmed = signal_raw[plot_start:plot_end]

    start_time_ns = df.iloc[start_idx]["time"]
    start_time = pd.to_datetime(start_time_ns)
    time = [start_time + timedelta(seconds=i / sampling_rate) for i in range(segment_length)]

    return signal_raw_trimmed, signal_cleaned_core, signal_cleaned_extended, time


def compute_autocorr_extended(cleaned_core, cleaned_extended, max_lag_sec, sampling_rate):
    """
    Compute extended autocorrelation for signal quality assessment.
    
    Calculates the correlation between the core signal and progressively shifted versions
    of the extended signal to identify periodicity at physiologically relevant intervals.
    
    Parameters
    ----------
    cleaned_core : numpy.ndarray
        Cleaned signal for the core segment
    cleaned_extended : numpy.ndarray
        Cleaned signal with additional padding for autocorrelation
    max_lag_sec : float
        Maximum lag time in seconds
    sampling_rate : int
        Sampling rate of the signal in Hz
    
    Returns
    -------
    tuple
        (normed_corrs, lags)
        - normed_corrs: Normalized autocorrelation values (0-1)
        - lags: Corresponding time lags in seconds
    
    Notes
    -----
    Uses a safe correlation calculation that handles edge cases like zero variance.
    The autocorrelation is normalized to have a maximum value of 1.0.
    """

    def safe_correlation(a, b):
        if np.std(a) == 0 or np.std(b) == 0:
            return 0.0
        return np.corrcoef(a, b)[0, 1]

    max_shift = int(max_lag_sec * sampling_rate)
    corrs = []
    for lag in range(max_shift):
        if lag + len(cleaned_core) > len(cleaned_extended):
            corrs.append(0)
        else:
            corr = safe_correlation(cleaned_core, cleaned_extended[lag:lag + len(cleaned_core)])
            corrs.append(corr)

    corrs = np.nan_to_num(np.array(corrs))
    normed_corrs = corrs / np.max(corrs) if np.max(corrs) > 0 else corrs
    return normed_corrs, np.arange(len(corrs)) / sampling_rate


def signal_quality_dashboard(df, signal_col, clean_func,
                                    signal_label="Signal",
                                    normalize_func=None,
                                    sampling_rate=200,
                                    segment_duration_sec=10,
                                    quality_lag_low=0.5,
                                    quality_lag_high=1.5,
                                    quality_threshold=0.6,
                                    max_lag_sec=3,
                                    clean_padding_ratio=0.2,
                                    delta_padding_sec=1.6):
    """
    Assess biosignal quality and return a DataFrame with timestamps and quality scores.
    
    This function evaluates signal quality by analyzing the autocorrelation of signal segments
    at physiologically relevant time lags. It returns a DataFrame containing timestamps and
    corresponding quality scores for each segment.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing signal data with a 'time' column (in pandas datetime format or nanoseconds)
    signal_col : str
        Column name containing the signal data
    clean_func : callable
        Function to clean the signal (e.g., nk.ppg_clean, nk.ecg_clean)
    sampling_rate : int, default=186
        Sampling rate of the signal in Hz
    segment_duration_sec : float, default=10
        Duration of each segment in seconds
    quality_lag_low : float, default=0.5
        Lower bound for lag range in seconds for quality assessment
        (typically based on physiological limits, e.g., min heart rate)
    quality_lag_high : float, default=1.5
        Upper bound for lag range in seconds for quality assessment
        (typically based on physiological limits, e.g., max heart rate)
    max_lag_sec : float, default=3
        Maximum lag to compute in the autocorrelation analysis
    clean_padding_ratio : float, default=0.2
        Ratio of segment length to use for padding during cleaning
    delta_padding_sec : float, default=1.6
        Additional padding in seconds for the extended segment
    normalize_func : callable, optional
        Function to normalize the signal (e.g., zscore_normalize)
    verbose : bool, default=False
        Whether to print progress information
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with 'time' and 'quality_score' columns, where:
        - time: start time of each segment
        - quality_score: quality score between 0-1 (higher is better)
    
    Notes
    -----
    Quality score is based on the maximum autocorrelation in the specified lag range,
    which captures the periodicity of the signal at physiologically expected intervals.
    """

    app = Dash(__name__)

    normalize_checkbox = dcc.Checklist(
        options=[{"label": "Normalize Signal", "value": "yes"}],
        id="normalize-signal", value=[]
    ) if normalize_func else html.Div()

    app.layout = html.Div([
        html.H2(f"{signal_label} Quality Dashboard"),

        dcc.Graph(id="signal-plot"),

        html.Label("Select Segment"),
        dcc.Slider(id='segment-slider', min=0,
                   max=len(df) - sampling_rate * segment_duration_sec,
                   step=sampling_rate * segment_duration_sec,
                   value=0,
                   tooltip={"placement": "bottom", "always_visible": True}),
        dcc.Checklist(
            options=[
                {"label": "Show Raw", "value": "raw"},
                {"label": "Show Cleaned", "value": "cleaned"}
            ],
            value=["cleaned"],
            id="show-options"
        ),
        normalize_checkbox,

        html.Div([
            html.Label("Quality Threshold"),
            dcc.Input(id="quality-input", type="number", value=quality_threshold, step=0.01)
        ], style={"marginTop": "15px"}),

        html.Div([
            html.Button("⬅️ Search Left", id="search-left", n_clicks=0,
                        style={"marginRight": "10px", "backgroundColor": "#f0f0f0", "padding": "8px 16px",
                               "border": "1px solid #ccc", "borderRadius": "5px"}),
            html.Button("Search Right ➡️", id="search-right", n_clicks=0,
                        style={"marginRight": "10px", "backgroundColor": "#f0f0f0", "padding": "8px 16px",
                               "border": "1px solid #ccc", "borderRadius": "5px"}),
            html.Button("✔️ Assess Quality", id="assess-btn", n_clicks=0,
                        style={"backgroundColor": "#DFF0D8", "padding": "8px 16px",
                               "border": "1px solid #ccc", "borderRadius": "5px"})
        ], style={"marginTop": "10px"}),

        html.Div(id="search-status", style={"color": "#888", "marginTop": "10px"}),

        html.Div(id="quality-output", style={"marginTop": "15px", "fontWeight": "bold"}),

        dcc.Graph(id="autocorr-plot"),
        dcc.Graph(id="shifted-plot")
    ])

    @app.callback(
        Output("signal-plot", "figure"),
        Input("segment-slider", "value"),
        Input("show-options", "value"),
        Input("normalize-signal", "value") if normalize_func else State("segment-slider", "value")
    )
    def update_signal_plot(start_idx, show_opts, normalize_signal):
        raw, cleaned_core, _, time = prepare_signal_segment(df, start_idx, signal_col, clean_func,
                                                             segment_duration_sec, sampling_rate,
                                                             delta_padding_sec, clean_padding_ratio)

        raw_viz, cleaned_viz = raw, cleaned_core
        if normalize_func and "yes" in normalize_signal:
            raw_viz = normalize_func(raw)
            cleaned_viz = normalize_func(cleaned_core)

        fig = go.Figure()
        if "raw" in show_opts:
            fig.add_trace(go.Scatter(x=time, y=raw_viz, mode='lines', name='Raw', line=dict(color='gray')))
        if "cleaned" in show_opts:
            fig.add_trace(go.Scatter(x=time, y=cleaned_viz, mode='lines', name='Cleaned', line=dict(color='blue')))
        fig.update_layout(title="Signal Segment", xaxis_title="Time", yaxis_title=signal_label)
        return fig

    @app.callback(
        [Output("autocorr-plot", "figure"),
         Output("shifted-plot", "figure"),
         Output("quality-output", "children")],
        Input("assess-btn", "n_clicks"),
        State("segment-slider", "value"),
        State("quality-input", "value")
    )
    def assess_quality(n, start_idx, quality_thresh):
        raw, cleaned_core, cleaned_ext, time = prepare_signal_segment(df, start_idx, signal_col, clean_func,
                                                                      segment_duration_sec, sampling_rate,
                                                                      delta_padding_sec, clean_padding_ratio)

        autocorr, lags = compute_autocorr_extended(cleaned_core, cleaned_ext,
                                                   max_lag_sec, sampling_rate)

        min_idx = int(quality_lag_low * sampling_rate)
        max_idx = int(quality_lag_high * sampling_rate)
        best_idx = np.argmax(autocorr[min_idx:max_idx]) + min_idx
        best_lag = lags[best_idx]
        best_score = float(np.nan_to_num(autocorr[best_idx]))

        auto_fig = go.Figure()
        auto_fig.add_trace(go.Scatter(x=lags, y=autocorr, mode='lines', name='Autocorrelation'))
        auto_fig.add_trace(go.Scatter(x=[best_lag], y=[best_score], mode='markers',
                                      marker=dict(color='red', size=10), name='Max Corr'))
        auto_fig.update_layout(title="Autocorrelation", xaxis_title="Lag (s)", yaxis_title="Normalized Corr")

        shifted = cleaned_ext[best_idx:best_idx + len(cleaned_core)]
        shift_fig = go.Figure()
        shift_fig.add_trace(go.Scatter(x=time, y=cleaned_core, mode='lines', name='Cleaned'))
        shift_fig.add_trace(go.Scatter(x=time, y=shifted, mode='lines',
                                       name=f'Shifted (Δt={best_lag:.2f}s)', line=dict(color='red')))
        shift_fig.update_layout(title="Shifted Signal", xaxis_title="Time", yaxis_title=signal_label)

        quality_text = f"Max correlation in [{quality_lag_low}s–{quality_lag_high}s] = {best_score:.2f} → " + \
                       ("Good ✅" if best_score >= quality_thresh else "Poor ❌")
        return auto_fig, shift_fig, quality_text

    @app.callback(
        Output("segment-slider", "value"),
        Output("search-status", "children"),
        Input("search-left", "n_clicks"),
        Input("search-right", "n_clicks"),
        State("segment-slider", "value"),
        State("quality-input", "value"),
        State("normalize-signal", "value") if normalize_func else State("segment-slider", "value")
    )
    def search_quality_segment(n_left, n_right, current_idx, quality_thresh, normalize_signal):
        triggered = ctx.triggered_id
        if triggered not in ["search-left", "search-right"]:
            return current_idx, ""

        direction = -1 if triggered == "search-left" else 1
        step = sampling_rate * segment_duration_sec
        new_idx = current_idx + step * direction

        while 0 <= new_idx <= len(df) - sampling_rate * segment_duration_sec:
            raw, cleaned_core, cleaned_ext, _ = prepare_signal_segment(df, new_idx, signal_col, clean_func,
                                                                       segment_duration_sec, sampling_rate,
                                                                       delta_padding_sec, clean_padding_ratio)

            autocorr, _ = compute_autocorr_extended(cleaned_core, cleaned_ext,
                                                    max_lag_sec, sampling_rate)

            min_idx = int(quality_lag_low * sampling_rate)
            max_idx = int(quality_lag_high * sampling_rate)
            best_score = np.nan_to_num(np.max(autocorr[min_idx:max_idx]))

            if best_score >= quality_thresh:
                return new_idx, ""

            new_idx += step * direction

        return current_idx, "No segment found with quality above threshold."

    app.run(debug=True, port='3443')








def assess_quality_percentage(df,
                   signal_col,
                   clean_func,
                   sampling_rate=186,
                   segment_duration_sec=10,
                   quality_lag_low=0.5,
                   quality_lag_high=1.5,
                   quality_threshold=0.6,
                   max_lag_sec=3,
                   clean_padding_ratio=0.2,
                   delta_padding_sec=1.6,
                   normalize_func=None,
                   signal_label="Signal",
                   launch_dashboard=False,
                   plot=None,
                   bin_size=0.1,
                   num_plots_bin=1,
                   verbose=False):
    """
    Assess biosignal quality and return the percentage of high-quality segments.
    
    This function evaluates signal quality across all segments and returns the percentage
    of segments that exceed the quality threshold. Optionally generates a comprehensive
    HTML report and launches an interactive dashboard.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing signal data with a 'time' column (in pandas datetime format or nanoseconds)
    signal_col : str
        Column name containing the signal data
    clean_func : callable
        Function to clean the signal (e.g., nk.ppg_clean, nk.ecg_clean)
    sampling_rate : int, default=186
        Sampling rate of the signal in Hz
    segment_duration_sec : float, default=10
        Duration of each segment in seconds
    quality_lag_low : float, default=0.5
        Lower bound for lag range in seconds for quality assessment
    quality_lag_high : float, default=1.5
        Upper bound for lag range in seconds for quality assessment
    quality_threshold : float, default=0.6
        Threshold for determining high-quality segments (0-1)
    max_lag_sec : float, default=3
        Maximum lag to compute in the autocorrelation analysis
    clean_padding_ratio : float, default=0.2
        Ratio of segment length to use for padding during cleaning
    delta_padding_sec : float, default=1.6
        Additional padding in seconds for the extended segment
    normalize_func : callable, optional
        Function to normalize the signal (e.g., zscore_normalize)
    signal_label : str, default="Signal"
        Label for signal in visualizations
    launch_dashboard : bool, default=False
        Whether to launch an interactive quality assessment dashboard
    plot : str, optional
        Path to save HTML report (if None, no report is generated)
    bin_size : float, default=0.1
        Bin size for quality score histogram in report
    num_plots_bin : int, default=1
        Number of example segments to plot per quality bin in report
    verbose : bool, default=False
        Whether to print progress information
    
    Returns
    -------
    float
        Percentage of segments with quality scores above the threshold
    
    Notes
    -----
    The HTML report (if generated) includes:
    - Overall quality summary
    - Binary quality heatmap
    - Continuous quality heatmap
    - Histogram of quality scores
    - Example segments for each quality bin
    """


    segment_len = segment_duration_sec * sampling_rate
    segment_indices = list(range(0, len(df) - segment_len, segment_len))
    quality_flags = []
    quality_scores = []
    timestamps = []
    segment_store = []

    if verbose:
        print("Assessing signal quality...")
    
    for idx in tqdm(segment_indices):
        try:
            _, cleaned_core, cleaned_ext, time = prepare_signal_segment(
                df, idx, signal_col, clean_func,
                segment_duration_sec, sampling_rate,
                delta_padding_sec, clean_padding_ratio
            )

            autocorr, _ = compute_autocorr_extended(cleaned_core, cleaned_ext,
                                                    max_lag_sec, sampling_rate)
            min_idx = int(quality_lag_low * sampling_rate)
            max_idx = int(quality_lag_high * sampling_rate)
            best_score = np.nan_to_num(np.max(autocorr[min_idx:max_idx]))

            quality_flags.append(1 if best_score >= quality_threshold else 0)
            quality_scores.append(best_score)
            timestamps.append(time[0])
            segment_store.append((time, cleaned_core, best_score))

        except Exception as e:
            quality_flags.append(0)
            quality_scores.append(0.0)
            timestamps.append(pd.to_datetime(df.iloc[idx]["time"]))
            segment_store.append(([], [], 0.0))

    quality_percent = (np.sum(quality_flags) / len(quality_flags)) * 100
    
    
    if verbose:
        print(f"\nQuality > {quality_threshold} in {quality_percent:.2f}% of segments.")
    
    
    # Plotting section
    if plot is not None:
        if verbose:
            print(f"Report saved to: {full_path}")

        # Heatmap of flags
        heatmap_flag = go.Figure(data=go.Heatmap(
            z=[quality_flags],
            x=[ts.strftime("%H:%M:%S") for ts in timestamps],
            colorscale="Viridis",
            colorbar=dict(title="Quality Flag"),
            showscale=True
        ))
        heatmap_flag.update_layout(
            title="Signal Quality Flag Heatmap",
            xaxis_title="Time",
            yaxis=dict(showticklabels=False),
            height=400
        )

        # Heatmap of scores
        heatmap_score = go.Figure(data=go.Heatmap(
            z=[quality_scores],
            x=[ts.strftime("%H:%M:%S") for ts in timestamps],
            colorscale="Plasma",
            colorbar=dict(title="Quality Score"),
            zmin=0,
            zmax=1,
            showscale=True
        ))
        heatmap_score.update_layout(
            title="Signal Quality Score Heatmap",
            xaxis_title="Time",
            yaxis=dict(showticklabels=False),
            height=400
        )

        # Histogram of quality scores
        hist_fig = go.Figure()
        hist_fig.add_trace(go.Histogram(
            x=quality_scores,
            xbins=dict(size=bin_size),
            marker_color='blue',
            opacity=0.75,
        ))
        hist_fig.update_layout(
            title="Histogram of Quality Scores",
            xaxis_title="Quality Score",
            yaxis_title="Count",
            bargap=0.1,
            width=1200
        )

        # Segment binning
        bins = np.arange(0, 1.0001 + bin_size, bin_size)
        bin_indices = {i: [] for i in range(len(bins) - 1)}
        for i, score in enumerate(quality_scores):
            for j in range(len(bins) - 1):
                if bins[j] <= score < bins[j + 1]:
                    bin_indices[j].append(i)
                    break

        segment_figs = []
        for bin_idx, indices in bin_indices.items():
            selected = indices[:num_plots_bin]
            for idx in selected:
                time, cleaned, score = segment_store[idx]
                if normalize_func is not None:
                    cleaned = normalize_func(cleaned)

                seg_fig = go.Figure()
                seg_fig.add_trace(go.Scatter(
                    x=time,
                    y=cleaned,
                    mode='lines',
                    name='Cleaned Signal',
                    line=dict(color='royalblue')
                ))
                seg_fig.update_layout(
                    title=f"Segment (Quality: {score:.2f}, Bin: {bins[bin_idx]:.2f}–{bins[bin_idx + 1]:.2f})",
                    xaxis_title="Time",
                    yaxis_title=signal_label,
                    margin=dict(l=20, r=20, t=40, b=20),
                    # width=1000,
                    height=300
                )
                segment_figs.append(seg_fig)

        # Save to HTML
        full_path = os.path.abspath(plot)
        with open(full_path, "w") as f:
            f.write('<html><head><title>Signal Quality Report</title></head><body>\n')
            f.write(f'<h1>Report</h1>')
            f.write(f'<h3 style="color: blue;">Segment Above Threshold({quality_threshold}): {quality_percent:.2f}%</h3>')
            f.write('<h2>Binary Quality Heatmap</h2>')
            f.write(heatmap_flag.to_html(full_html=False, include_plotlyjs='cdn'))
            f.write('<hr><h2>Continuous Quality Heatmap</h2>')
            f.write(heatmap_score.to_html(full_html=False, include_plotlyjs=False))
            f.write('<hr><h2>Histogram of Quality Scores</h2>')
            f.write(hist_fig.to_html(full_html=False, include_plotlyjs=False))

            f.write('<hr><h2>Segment Plots by Quality Bins</h2>')
            for fig in segment_figs:
                f.write('<div style="margin-bottom:40px;">')
                f.write(fig.to_html(full_html=False, include_plotlyjs=False))
                f.write('</div>')

            f.write('</body></html>')

        print(f"📁 Report saved to: {full_path}")

    # Launch dashboard
    if launch_dashboard:
        signal_quality_dashboard(
            df=df,
            signal_col=signal_col,
            clean_func=clean_func,
            normalize_func=normalize_func,
            sampling_rate=sampling_rate,
            segment_duration_sec=segment_duration_sec,
            quality_lag_low=quality_lag_low,
            quality_lag_high=quality_lag_high,
            quality_threshold=quality_threshold,
            max_lag_sec=max_lag_sec,
            clean_padding_ratio=clean_padding_ratio,
            delta_padding_sec=delta_padding_sec,
            signal_label=signal_label
        )

    return quality_percent




def zscore_normalize(signal):
    return (signal - np.mean(signal)) / np.std(signal)



def assess_quality(df,
                  signal_col,
                  clean_func,
                  sampling_rate=186,
                  step_size_sec=1,
                  segment_duration_sec=10,
                  quality_lag_low=0.5,
                  quality_lag_high=1.5,
                  max_lag_sec=3,
                  clean_padding_ratio=0.2,
                  delta_padding_sec=1.6,
                  verbose=True):
    """
    Assess biosignal quality and return a DataFrame with timestamps and quality scores.
    
    This function evaluates signal quality by analyzing the autocorrelation of signal segments
    at physiologically relevant time lags. It returns a DataFrame containing timestamps and
    corresponding quality scores for each segment.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing signal data with a 'time' column (in pandas datetime format or nanoseconds)
    signal_col : str
        Column name containing the signal data
    clean_func : callable
        Function to clean the signal (e.g., nk.ppg_clean, nk.ecg_clean)
    sampling_rate : int, default=186
        Sampling rate of the signal in Hz
    segment_duration_sec : float, default=10
        Duration of each segment in seconds
    quality_lag_low : float, default=0.5
        Lower bound for lag range in seconds for quality assessment
        (typically based on physiological limits, e.g., min heart rate)
    quality_lag_high : float, default=1.5
        Upper bound for lag range in seconds for quality assessment
        (typically based on physiological limits, e.g., max heart rate)
    max_lag_sec : float, default=3
        Maximum lag to compute in the autocorrelation analysis
    clean_padding_ratio : float, default=0.2
        Ratio of segment length to use for padding during cleaning
    delta_padding_sec : float, default=1.6
        Additional padding in seconds for the extended segment
    normalize_func : callable, optional
        Function to normalize the signal (e.g., zscore_normalize)
    verbose : bool, default=False
        Whether to print progress information
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with 'time' and 'quality_score' columns, where:
        - time: start time of each segment
        - quality_score: quality score between 0-1 (higher is better)
    
    Notes
    -----
    Quality score is based on the maximum autocorrelation in the specified lag range,
    which captures the periodicity of the signal at physiologically expected intervals.
    """
    # segment_len = segment_duration_sec * sampling_rate
    # segment_indices = list(range(0, len(df) - segment_len, segment_len))

    segment_len = segment_duration_sec * sampling_rate
    step_size = int(step_size_sec * sampling_rate)  # Convert step size to samples
    
    # Calculate segment indices with overlapping windows based on step_size
    segment_indices = list(range(0, len(df) - segment_len, step_size))

    quality_scores = []
    timestamps = []
    
    if verbose:
        print("Assessing signal quality...")
        iterator = tqdm(segment_indices)
    else:
        iterator = segment_indices
    
    for idx in iterator:
        try:
            _, cleaned_core, cleaned_ext, time = prepare_signal_segment(
                df, idx, signal_col, clean_func,
                segment_duration_sec, sampling_rate,
                delta_padding_sec, clean_padding_ratio
            )
            autocorr, _ = compute_autocorr_extended(cleaned_core, cleaned_ext,
                                                  max_lag_sec, sampling_rate)
            min_idx = int(quality_lag_low * sampling_rate)
            max_idx = int(quality_lag_high * sampling_rate)
            best_score = np.nan_to_num(np.max(autocorr[min_idx:max_idx]))
            quality_scores.append(best_score)
            timestamps.append(time[0])
        except Exception as e:
            quality_scores.append(0.0)
            timestamps.append(df.iloc[idx]["time"])
    
    # Create DataFrame with time and quality scores
    quality_df = pd.DataFrame({
        'time': timestamps,
        'quality_score': quality_scores
    })
    
    return quality_df
