from __future__ import annotations
from typing import Any, Dict, Optional, TypedDict
import ipywidgets as wg
import pandas as pd
import plotly.graph_objects as go

from ..mascope_data.wrapper import MascopeDataWrapper


class CallbackContext(TypedDict):
    """TypedDict for storing callback context attributes"""

    fig: go.FigureWidget  # FigureWidget to be used for click events
    click_output: wg.Output  # Output widget for displaying outputs
    dataset: MascopeDataWrapper  # Dataset containing wider set of dataframes
    reference_df: pd.DataFrame | None  # Reference DataFrame used for figure building
    x_axis: str | None  # Name of the x-axis column in the reference DataFrame
    y_axis: str | None  # Name of the y-axis column in the reference DataFrame
    clicked_dots_data: dict  # Clicked data points from reference DataFrame
    marker_points_idx: dict  # Clicked data points indices
    original_symbols: dict  # Original marker symbols
    original_colors: dict  # Original marker colors
    figure_stash: dict  # Cache for figures


class ClickEventHandler:
    """
    Class to handle click events in given figure.
    """

    def __init__(
        self,
        fig: go.FigureWidget,
        out: wg.Output,
        dataset: MascopeDataWrapper,
        callback_func: callable | None = None,
        reference_df: pd.DataFrame | None = None,
        x_axis: str | None = None,
        y_axis: str | None = None,
    ) -> None:
        """
        Initialize ClickEventHandler with given figure and output widget.

        :param fig: go.FigureWidget which traces contains marker-points.
        :type fig: go.FigureWidget
        :param out: Output widget for displaying outputs.
        :type out: Output
        :param dataset: Dataset to be used for the click event.
        :type dataset: MascopeDataWrapper
        :param callback_func: Callback function to execute when a point is clicked.
        :type callback_func: callable | None
        :param reference_df: Optional reference DataFrame for additional data.
        :type reference_df: pd.DataFrame | None
        :param x_axis: Name of the x-axis column in the dataset.
        :type x_axis: str | None
        :param y_axis: Name of the y-axis column in the dataset.
        :type y_axis: str | None
        :raises TypeError: if callback_func is not callable or is None
        """

        self.callback_func = callback_func
        self.out = out
        if not callable(self.callback_func):
            raise TypeError("callback_func is not callable or is None.")
        # Set the callback context for click events
        self.callback_context: CallbackContext = {
            "fig": fig,
            "click_output": out,
            "reference_df": reference_df,
            "dataset": dataset,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "clicked_dots_data": {},  # {trace_name: [clicked_data_points]}
            "marker_points_idx": {},  # {trace_name: [clicked_data_points_indices]}
            "original_symbols": {},  # {trace_name: original_marker_symbols}
            "original_colors": {},  # {trace_name: original_marker_colors}
            "figure_stash": {},  # {trace_name: figure_stash}
        }

    def click_callback(
        self,
        trace: go.Trace,
        points: dict,
        selector: Optional[Dict[str, Any]],  # pylint: disable=unused-argument
    ) -> None:
        """Set a callback function to be executed when a point is clicked.

        :param trace: clicked trace
        :type trace: go.Trace
        :param points: clicked points
        :type points: dict
        :param selector: A dictionary used to filter which traces trigger the event.
        :type selector: Optional[Dict[str, Any]]
        """

        if not points or not points.xs or not points.point_inds:
            return
        # Collect points from the clicked data
        point_index = points.point_inds[0]
        clicked_point = {
            "trace_name": trace.name if hasattr(trace, "name") else "unknown_trace",
            "point_index": point_index,
            "x_value": trace.x[point_index],
            "y_value": trace.y[point_index],
        }
        # Check if all required optional inputs are provided
        missing_inputs = []
        if self.callback_context.get("reference_df") is None:
            missing_inputs.append("reference_df")
        if self.callback_context.get("x_axis") is None:
            missing_inputs.append("x_axis")
        if self.callback_context.get("y_axis") is None:
            missing_inputs.append("y_axis")
        with self.out:
            self.out.clear_output()
            if missing_inputs:
                print("Clicked Point:", clicked_point)
                print(
                    f"Missing inputs: {', '.join(missing_inputs)}. "
                    "Provide these inputs for additional functionality."
                )
                return
            # If all inputs are provided, call the callback function
            self.callback_func(
                clicked_point=clicked_point, callback_context=self.callback_context
            )
