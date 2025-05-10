from typing import List
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from colorcet import glasbey as colorvector

from ..plot_tools import hover_string

from ..mascope_data.wrapper import MascopeDataWrapper


class SpectrumPlotter:
    """
    Class containing functions to build spectrum related traces
    by utlizing dataset with SpectrumDataExtension -extension."""

    def __init__(self, dataset: MascopeDataWrapper):
        """
        Initialize dataset to self

        :param dataset: MascopeDataWrapper -dataset with
        SpectrumDataExtension- extension.
        :type dataset: MascopeDataWrapper
        """
        self.dataset = dataset
        self.hoverbox_columns = [
            "sample_item_id",
            "intensity",
            "unit",
            "datetime",
            "sample_item_name",
            "sample_item_type",
            "instrument",
        ]  # List of HoverBox columns

    def get_spectrum_traces(
        self,
        sample_file_id: str,
        mz_min: float = None,
        mz_max: float = None,
        t_min: float = None,
        t_max: float = None,
    ) -> List[go.Scatter]:
        """
        Get spectrum traces for a specific sample file id.

        :param sample_file_id: sample file id
        :type sample_file_id: str
        :param mz_min: mz range low end, defaults to None
        :type mz_min: float, optional
        :param mz_max: mz range high end, defaults to None
        :type mz_max: float, optional
        :param t_min: time starting point, defaults to None
        :type t_min: float, optional
        :param t_max: time ending point, defaults to None
        :type t_max: float, optional
        :raises ValueError: if sample file id can't be found
        from match_samples
        :return: spectrum trace
        :rtype: go.Scatter
        """

        traces = []
        sample_file_ids = self.dataset.match_samples.sample_file_id.unique()

        match sample_file_id:
            case _ if sample_file_id in sample_file_ids:
                spectrum_df = self.dataset.get_spectrum_data(
                    sample_file_id=sample_file_id,
                    mz_min=mz_min,
                    mz_max=mz_max,
                    t_min=t_min,
                    t_max=t_max,
                )
                # Get sample name and order number for colorcoding
                sample_name, sample_order = self._get_sample_name_and_order_number(
                    sample_file_id=sample_file_id
                )
                spectrum_trace = self.spectrum_trace(
                    df_group=spectrum_df,
                    group_name=sample_name,
                    color=colorvector[sample_order],
                )
                traces.append(spectrum_trace)
            case _:  # Handle unknown sample values
                raise ValueError(f"Sample {sample_name} not found in match_samples.")

        return traces

    def base_spectrum_figure(
        self,
    ) -> go.FigureWidget:
        """
        Build base FigureWidget and setup layout

        :return: figurewidget which is ready for adding traces
        :rtype: go.FigureWidget
        """

        fig = go.FigureWidget()
        layout = self.build_layout()
        fig.update_layout(layout)
        return fig

    def spectrum_trace(
        self,
        df_group: pd.DataFrame,
        group_name: str,
        color: str = None,
    ) -> go.Scatter:
        """
        Builds spectrum traces

        :param df_group: dataframe containing at least columns:
        -'mz'
        -'intensity'
        - and columns in self.hoverbox_columns
        :type df_group: pd.DataFrame
        :param group_name: trace-group name
        :type group_name: str
        :param color: color for trace-group, defaults to None
        :type color: str, optional
        :return: scatter spectrum traces
        :rtype: go.Scatter
        """

        hover_items = hover_string(self.hoverbox_columns)
        df_group = df_group.sort_values(by="mz", ascending=True)
        if df_group["intensity"].sum() != 0:
            spectrum = go.Scatter(
                x=df_group["mz"],
                y=df_group["intensity"],
                mode="lines",
                name=str(group_name),
                marker={"symbol": np.repeat("circle", len(df_group))},
                customdata=df_group[self.hoverbox_columns],
                hovertemplate=hover_items,
                line={"color": color} if color else {},
                visible=True,
                legendgroup=group_name,  # Group legend items
            )
            return spectrum

    def build_layout(
        self,
    ) -> dict:
        """
        Build the layout of the figure and return layout.

        :param fig: plotly-figure containing traces
        :type fig: go.FigureWidget
        :return: layout dictionary to be applied to the figure
        :rtype: dict
        """
        # Check if intensity_unit is available
        intensity_unit = getattr(self.dataset, "intensity_unit", None)
        yaxis_title = (
            f"Signal intensity ({intensity_unit})"
            if intensity_unit
            else "Signal intensity"
        )
        layout_dict = {
            "showlegend": True,
            "xaxis": {
                "showspikes": True,
                "spikecolor": "black",
                "showline": True,
                "linewidth": 1,
                "linecolor": "black",
                "ticks": "outside",
                "tickwidth": 1,
                "tickcolor": "black",
                "ticklen": 5,
                "rangeslider_visible": True,
            },
            "yaxis": {
                "showspikes": True,
                "spikecolor": "black",
                "showline": True,
                "linewidth": 1,
                "linecolor": "black",
                "ticks": "outside",
                "tickwidth": 1,
                "tickcolor": "black",
                "ticklen": 5,
                "title_text": yaxis_title,
            },
            "updatemenus": [
                {
                    "buttons": [
                        {
                            "label": "Linear Scale",
                            "method": "relayout",
                            "args": ["yaxis.type", "linear"],
                        },
                        {
                            "label": "Log Scale",
                            "method": "relayout",
                            "args": ["yaxis.type", "log"],
                        },
                    ],
                    "direction": "down",
                    "showactive": True,
                    "x": 0.05,
                    "y": 1.5,
                }
            ],
        }

        return layout_dict

    def _get_sample_name_and_order_number(self, sample_file_id: str) -> list[str, int]:
        """
        Get sample name and alphapetical order number by using
        'sample_file_id' and 'match_samples' -dataframe.

        :param sample_file_id: mascope database 'sample_file_id' value
        for sample under intrest
        :type sample_file_id: str
        :return: sample_item_name_datetime and alphapetical order number of
        'sample_file_id' (can be used for colorcoding trace-groups)
        :rtype: list[str, int]
        """

        sample_name = self.dataset.match_samples["sample_item_name_datetime"][
            self.dataset.match_samples.sample_file_id == sample_file_id
        ].unique()[0]
        sample_order = {
            v: i + 1
            for i, v in enumerate(
                sorted(self.dataset.match_samples.sample_file_id.unique())
            )  # Create dictionary with order number for each sample file id
        }.get(
            sample_file_id
        )  # Get the integer order number for the given target compound i

        return sample_name, sample_order
