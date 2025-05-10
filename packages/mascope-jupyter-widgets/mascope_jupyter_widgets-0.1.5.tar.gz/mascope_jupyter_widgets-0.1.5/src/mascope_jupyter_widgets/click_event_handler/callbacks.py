import pandas as pd
from ipyaggrid import Grid
from IPython.display import display
from .helpers import (
    get_trace_and_initialize_storage,
    extract_reference_data,
    merge_clicked_points_with_match_data,
    collect_spectrum_traces,
    update_marker_symbols_and_colors,
    restore_original_markers,
)
from ..widgets_config import (
    GRID_OPTIONS,
)
from ..spectrum.plots import SpectrumPlotter


# Callback function
def display_reference_table(
    clicked_point: dict, callback_context: dict, update_markers: bool = True
) -> None:
    """
    Display the reference table for the clicked point.

    :param clicked_point: Dictionary containing clicked point data.
    :rtype clicked_point: dict
    :param callback_context: Dictionary containing the callback context.
    :rtype callback_context: dict
    :param update_markers: Flag to indicate whether to update markers or not.
    :type update_markers: bool
    """
    # Extract trace name and context from the clicked point
    context = callback_context
    trace_name = clicked_point["trace_name"]
    try:
        trace = get_trace_and_initialize_storage(trace_name, context)
    except ValueError:
        print(f"Trace '{trace_name}' not found.")
        return
    selected_data = extract_reference_data(clicked_point, context)
    if selected_data.empty:
        print(f"No matching data for trace '{trace_name}'.")
        if update_markers:
            restore_original_markers(
                trace_name,
                trace,
                context["fig"],
                context["original_symbols"],
                context["original_colors"],
            )
        return
    # Store clicked data points and marker indices
    context["clicked_dots_data"][trace_name].append(selected_data)
    context["marker_points_idx"][trace_name].append(clicked_point["point_index"])
    if update_markers:
        update_marker_symbols_and_colors(
            trace_name,
            trace,
            context["marker_points_idx"],
            context["original_symbols"],
            context["original_colors"],
            context["fig"],
        )
    # Display part of the reference table
    clicked_points_compound_trace_df = pd.concat(
        context["clicked_dots_data"][trace_name], ignore_index=True
    ).drop_duplicates()
    display(
        Grid(
            grid_data=clicked_points_compound_trace_df,
            grid_options=GRID_OPTIONS,
            height=600,
        )
    )


# Callback function
def display_spectrum(
    clicked_point: dict, callback_context: dict, update_markers: bool = True
) -> None:
    """
    Process and display spectrum traces from clicked dot.

    :param clicked_point: Dictionary containing clicked point data.
    :type clicked_point: dict
    :param callback_context: Dictionary containing the callback context.
    :type callback_context: dict
    :param update_markers: Flag to indicate whether to update markers or not.
    :type update_markers: bool
    """
    # Extract trace name and context from the clicked point
    context = callback_context
    trace_name = clicked_point["trace_name"]  # Extract trace name
    if not hasattr(context["dataset"], "get_spectrum_data"):
        raise AttributeError(
            "The dataset object does not have the required method 'get_spectrum_data'. "
            "Please ensure the dataset is extended with SpectrumDataExtension."
        )
    spectrum_plotter = SpectrumPlotter(dataset=context["dataset"])
    try:
        trace = get_trace_and_initialize_storage(trace_name, context)
    except ValueError:
        print(f"Trace '{trace_name}' not found.")
        return
    # Collect reference data for the clicked point
    selected_data = extract_reference_data(clicked_point, context)
    if selected_data.empty:
        print(f"No matching data for trace '{trace_name}'.")
        if update_markers:
            restore_original_markers(
                trace_name,
                trace,
                context["fig"],
                context["original_symbols"],
                context["original_colors"],
            )
        return
    # Store clicked data points and marker indices
    context["clicked_dots_data"][trace_name].append(selected_data)
    context["marker_points_idx"][trace_name].append(clicked_point["point_index"])
    if update_markers:
        update_marker_symbols_and_colors(
            trace_name,
            trace,
            context["marker_points_idx"],
            context["original_symbols"],
            context["original_colors"],
            context["fig"],
        )
    # Combine all clicked points for same trace into a single DataFrame
    clicked_points_compound_trace_df = pd.concat(
        context["clicked_dots_data"][trace_name], ignore_index=True
    ).drop_duplicates()
    # Merge clicked points with match data
    required_columns = ["target_compound_id", "sample_item_id", "mz"]
    if not all(
        col in clicked_points_compound_trace_df.columns for col in required_columns
    ):
        merged_df = merge_clicked_points_with_match_data(
            clicked_points_compound_trace_df, context, required_columns
        )
    else:
        merged_df = clicked_points_compound_trace_df
    if merged_df.empty:
        print(f"No spectrum data available for trace '{trace_name}'.")
        return
    # Check if the trace_name is in the spectrum figure cache
    if trace_name not in context["figure_stash"]:
        context["figure_stash"][trace_name] = {}
    spectrum_traces = collect_spectrum_traces(
        merged_df, trace_name, context, spectrum_plotter
    )
    spectrum_fig = spectrum_plotter.base_spectrum_figure()
    spectrum_fig.add_traces(spectrum_traces)
    spectrum_fig.update_layout(title=trace_name)
    display(spectrum_fig)
