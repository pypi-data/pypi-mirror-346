import ipywidgets as wg
from IPython.display import display

from .plots import SpectrumPlotter
from .extension import SpectrumDataExtension

from ..mascope_data.wrapper import MascopeDataWrapper
from ..logging_config import logger  # Import the shared logger


class SpectrumWidget:
    """
    Builds widget selector for spectrum plots.
    """

    def __init__(
        self,
        dataset: MascopeDataWrapper,
    ):
        """
        Set up interactive widget-selector for spectrum figures.

        :param dataset: MascopeDataWrapper -dataset
        :type dataset: MascopeDataWrapper
        """

        self.dataset = dataset
        self.dataset.extend(SpectrumDataExtension)
        self.spectrum_plots = SpectrumPlotter(dataset=self.dataset)
        self.spectrum_figure = wg.Output()
        # Setup widget-selector
        self.create_figure_output()
        self.display_layout()

        self.dataset.add_observer("data_loaded", self.on_data_loaded)

        # Populate widgets with data if data is already loaded
        if self.dataset.data_loaded:
            self.on_data_loaded({"new": True})  # Simulate a change event

    def display_layout(self) -> None:
        """Displays the widget layout."""
        display(self.spectrum_figure)

    def create_figure_output(self) -> None:
        """Build output containing plotly figure layout"""
        try:
            logger.debug("Creating base spectrum figure.")
            self.fig = self.spectrum_plots.base_spectrum_figure()
            with self.spectrum_figure:
                display(self.fig)
            logger.debug("Base spectrum figure created successfully.")
        except (AttributeError, ValueError, TypeError) as e:
            logger.error(
                "Error in %s.%s: %s",
                self.__class__.__name__,
                "create_figure_output",
                e,
            )

    def update_figures(self, change=None) -> None:  # pylint: disable=unused-argument
        """Updates figure traces based on data."""

        try:
            logger.debug("Updating spectrum figure traces.")
            match_samples = self.dataset.match_samples

            with self.fig.batch_update():
                self.fig.data = []
                logger.debug("Cleared existing traces from the spectrum figure.")
                for (
                    sample_file_id
                ) in (
                    match_samples.sample_file_id.unique()
                ):  # Loop through unique sample_file_ids
                    logger.debug("Processing sample_file_id: %s", sample_file_id)
                    traces = self.spectrum_plots.get_spectrum_traces(
                        sample_file_id=sample_file_id,
                    )
                    self.fig.add_traces(traces)
                    logger.debug(f"Added traces for sample_file_id: {sample_file_id}")
            logger.debug("Spectrum figure traces updated successfully.")
        except (AttributeError, ValueError, TypeError) as e:
            logger.error(
                "Error in %s.%s: %s",
                self.__class__.__name__,
                "update_figures",
                e,
            )

    def on_clear_cache(self, change) -> None:  # pylint: disable=unused-argument
        """
        Callback for when `memory_cleared` changes.
        React to clearing the cache.
        - When the cache is cleared, updates the figure traces.
        """
        try:
            logger.info("Cache cleared. Updating spectrum figure traces.")
            self.update_figures()
            logger.info(
                "Spectrum figure traces updated successfully after cache clear."
            )
        except (AttributeError, ValueError, TypeError) as e:
            logger.error("Error in on_clear_cache: %s", e)

    def on_data_loaded(self, change) -> None:
        """
        Callback for when `data_loaded` changes.
        React to data being cleared or loaded.
        - If new data is loaded, updates figure traces.
        - If data is cleared, removes traces and reset figure to base.

        :param change: The change event dictionary.
        :type change: dict
        """
        try:
            if change["new"]:  # If data_loaded is True
                logger.info("Data loaded. Preparing to update spectrum figure traces.")
                self.dataset.add_observer("memory_cleared", self.on_clear_cache)
                logger.debug(
                    f"Observer for `memory_cleared` attached to {self.__class__.__name__}"
                    " on_clear_cache"
                )
                self.update_figures()
                logger.info(
                    "Spectrum figure traces updated successfully after data load."
                )
            else:
                logger.info("Data cleared. Resetting spectrum figure to base state.")
                self.reset_figure()
                logger.info("Spectrum figure reset to base state successfully.")
        except (AttributeError, ValueError, TypeError) as e:
            logger.error(
                "Error in %s.%s: %s",
                self.__class__.__name__,
                "on_data_loaded",
                e,
            )

    def reset_figure(self) -> None:
        """
        Reset the figure to its base state when data is not loaded.
        """
        try:
            logger.debug("Resetting spectrum figure to base state.")
            with self.spectrum_figure:
                self.fig.data = []
                logger.debug("Cleared all traces from the spectrum figure.")
                layout = self.spectrum_plots.build_layout()
                self.fig.update_layout(layout)
                logger.debug("Spectrum figure layout reset successfully.")
        except (
            AttributeError,
            ValueError,
            TypeError,
        ) as e:
            logger.error(
                "Error in %s.%s: %s",
                self.__class__.__name__,
                "reset_figure",
                e,
            )
