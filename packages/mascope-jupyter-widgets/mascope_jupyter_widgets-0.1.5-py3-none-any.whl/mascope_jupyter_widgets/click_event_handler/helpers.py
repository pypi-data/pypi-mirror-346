from __future__ import annotations
import re
from typing import TYPE_CHECKING
import pandas as pd
import numpy as np
import plotly.graph_objects as go

if TYPE_CHECKING:
    from ..spectrum.plots import SpectrumPlotter


# Helper function
def get_trace_and_initialize_storage(trace_name: str, context: dict) -> go.Trace:
    """
    Locate the trace in the figure and initialize storage for clicked points.

    :param trace_name: Name of the trace.
    :type trace_name: str
    :param context: Callback context containing the figure and storage.
    :type context: dict
    :return: The located trace.
    :rtype: go.Trace
    """
    trace = next((t for t in context["fig"].data if t.name == trace_name), None)
    if not trace:
        raise ValueError(f"Trace '{trace_name}' not found.")
    # Initialize storage for clicked points if not already present
    if trace_name not in context["clicked_dots_data"]:
        context["clicked_dots_data"][trace_name] = []
        context["marker_points_idx"][trace_name] = []
        marker = trace.marker
        context["original_symbols"][trace_name] = (
            list(marker.symbol)
            if isinstance(marker.symbol, (list, np.ndarray))
            else [marker.symbol] * len(trace.x)
        )
        context["original_colors"][trace_name] = (
            list(marker.color)
            if isinstance(marker.color, (list, np.ndarray))
            else [marker.color] * len(trace.x)
        )
    return trace


# Helper function
def extract_reference_data(clicked_point: dict, context: dict) -> pd.DataFrame:
    """
    Extract and validate reference data for the clicked point.

    :param clicked_point: Dictionary containing clicked point data.
    :type clicked_point: dict
    :param context: Callback context containing the reference DataFrame.
    :type context: dict
    :return: The extracted reference data.
    :rtype: pd.DataFrame
    """

    x_value, y_value = clicked_point["x_value"], clicked_point["y_value"]
    ref_df = pd.DataFrame(context["reference_df"])
    # Handle datetime localization if necessary
    if (context["x_axis"] == "datetime") and (ref_df[context["x_axis"]].dt.tz is None):
        ref_df[context["x_axis"]] = ref_df[context["x_axis"]].dt.tz_localize("UTC")
    # Find matching data points in the reference DataFrame
    selected_data = ref_df[
        (ref_df[context["x_axis"]] == x_value) & (ref_df[context["y_axis"]] == y_value)
    ]

    return selected_data


# Helper function
def find_dataset_property_with_columns(
    dataset: object, required_columns: list
) -> pd.DataFrame:
    """
    Find a property in the dataset object that is a DataFrame
    and contains the required columns.

    :param dataset: The dataset object to search.
    :type dataset: object
    :param required_columns: List of required column names.
    :type required_columns: list
    :return: The matching DataFrame.
    :rtype: pd.DataFrame
    :raises ValueError: If no matching DataFrame is found.
    """
    for _, attr in dataset.__dict__.items():
        if isinstance(attr, pd.DataFrame) and all(
            col in attr.columns for col in required_columns
        ):
            return attr
    raise ValueError(
        f"No property in the dataset contains all required columns: {', '.join(required_columns)}"
    )


# Helper function
def update_marker_symbols_and_colors(
    trace_name: str,
    trace: go.Trace,
    marker_points: dict,
    original_symbols: dict,
    original_colors: dict,
    fig: go.FigureWidget,
) -> None:
    """
    Update the marker symbols and colors for a trace.

    :param trace_name: Name of the trace.
    :type trace_name: str
    :param trace: The trace object.
    :type trace: go.Trace
    :param marker_points: Dictionary of marker points.
    :type marker_points: dict
    :param original_symbols: Dictionary of original marker symbols.
    :type original_symbols: dict
    :param original_colors: Dictionary of original marker colors.
    :type original_colors: dict
    :param fig: The Plotly figure widget.
    :type fig: go.FigureWidget
    """
    msymbols = original_symbols[trace_name][:]
    mcolors = original_colors[trace_name][:]
    for idx in marker_points[trace_name]:
        msymbols[idx], mcolors[idx] = "star", "black"
    with fig.batch_update():
        trace.marker.symbol = msymbols
        trace.marker.color = mcolors


# Helper function
def restore_original_markers(
    trace_name: str,
    trace: go.Trace,
    fig: go.FigureWidget,
    original_symbols: dict,
    original_colors: dict,
) -> None:
    """
    Restore the original marker symbols and colors for a trace.

    :param trace_name: Name of the trace.
    :type trace_name: str
    :param trace: The trace object.
    :type trace: go.Trace
    :param fig: The Plotly figure widget.
    :type fig: go.FigureWidget
    :param original_symbols: Dictionary of original marker symbols.
    :type original_symbols: dict
    :param original_colors: Dictionary of original marker colors.
    :type original_colors: dict
    """
    with fig.batch_update():
        trace.marker.symbol = original_symbols[trace_name]
        trace.marker.color = original_colors[trace_name]


# Helper function
def merge_clicked_points_with_match_data(
    clicked_points_df: pd.DataFrame, context: dict, required_columns: list
) -> pd.DataFrame:
    """
    Merge the clicked points DataFrame with the match data from the dataset.

    :param clicked_points_df: DataFrame containing clicked points.
    :type clicked_points_df: pd.DataFrame
    :param context: Callback context containing the dataset.
    :type context: dict
    :param required_columns: List of required columns for the match data.
    :type required_columns: list
    :return: Merged DataFrame.
    :rtype: pd.DataFrame
    """

    target_compound_id = clicked_points_df.target_compound_id.iloc[0]
    # Handle untarget peaks in target_compound_id
    if pd.isna(target_compound_id):
        # Use trace_names column to extract numeric values
        trace_names = clicked_points_df["trace_name"].fillna("")
        numeric_values = (
            trace_names.apply(
                lambda x: re.findall(r"\b\d+\.\d+\b", x)
            )  # Extract numeric values
            .explode()  # Flatten lists of numbers
            .dropna()
            .astype(float)
        )
        peak = numeric_values.iloc[0]
        # Filter the dataset using the peak ± 0.05 range
        dataset = context["dataset"]
        peak_data = dataset.peaks_matched
        filtered_data = peak_data[
            (peak_data["mz"] >= peak - 0.05) & (peak_data["mz"] <= peak + 0.05)
        ]
        # Merge the filtered data with clicked_points_df
        return pd.merge(
            clicked_points_df,
            filtered_data,
            on=["sample_item_id"],
            how="inner",
        )
    # Handle cases where "mz" is not in clicked_points_df columns
    if "mz" not in clicked_points_df.columns:
        match_data = find_dataset_property_with_columns(
            context["dataset"], required_columns
        )
        return pd.merge(
            clicked_points_df,
            match_data,
            on=["target_compound_id", "sample_item_id"],
            how="inner",
        )
    # Default case: return the clicked_points_df as is
    return clicked_points_df


# Helper function
def collect_spectrum_traces(
    merged_df: pd.DataFrame,
    trace_name: str,
    context: dict,
    spectrum_plotter: SpectrumPlotter,
) -> list:
    """
    Collect spectrum traces for each sample_file_id in the merged DataFrame.

    :param merged_df: Merged DataFrame containing spectrum data.
    :type merged_df: pd.DataFrame
    :param trace_name: Name of the trace.
    :type trace_name: str
    :param context: Callback context containing the spectrum cache.
    :type context: dict
    :param spectrum_plotter: SpectrumPlotter instance for generating traces.
    :type spectrum_plotter: SpectrumPlotter
    :return: List of spectrum traces.
    :rtype: list
    """
    spectrum_traces = []
    if trace_name not in context["figure_stash"]:
        context["figure_stash"][trace_name] = {}
    for sample_file_id in merged_df["sample_file_id"].unique():
        if sample_file_id in context["figure_stash"][trace_name]:
            spectrum_traces.extend(context["figure_stash"][trace_name][sample_file_id])
        else:
            round_df = merged_df[merged_df["sample_file_id"] == sample_file_id]
            mz_min, mz_max = (round_df.mz.min() - 0.05), (round_df.mz.max() + 0.05)
            new_traces = spectrum_plotter.get_spectrum_traces(
                sample_file_id,
                mz_min=mz_min,
                mz_max=mz_max,
            )
            spectrum_traces.extend(new_traces)
            context["figure_stash"][trace_name][sample_file_id] = new_traces

    return spectrum_traces
