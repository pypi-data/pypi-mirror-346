from typing import Dict, Any
import pandas as pd
import numpy as np
import pandera as pa

from .schemas import (
    spectrum_schema,
    add_column_for_filtering,
    set_unique_index,
    calculate_tic_norm_intensity_and_cumsum_tic_ratio,
)
from ..mascope_data.access import (
    get_mjw_mode,
)

MJW_DEV_MODE = get_mjw_mode()  # Get the MJW_DEV_MODE environment variable


class SpectrumDataExtension:
    """
    Spectrum related data extension for MascopeDataWrapper.
    When wrapped with MascopeDataWrapper, this extension provides
    additional methods to access spectrum data.
    """

    def __init__(self) -> None:
        """Initialize the SpectrumDataExtension class."""
        self.cached_samples_spectra: Dict[str, Dict[str, Any]] = {}
        self.cached_spectrum_params: Dict[str, Any] = (
            {  # Dictionary to store spectrum parameters
                "mz_min": None,
                "mz_max": None,
                "t_min": None,
                "t_max": None,
                "sample_file_id": None,
            }
        )

    def get_spectrum_data(
        self,
        sample_file_id: str = None,
        mz_min: float = None,
        mz_max: float = None,
        t_min: float = None,
        t_max: float = None,
    ) -> pd.DataFrame:
        """
        Get spectrum data for a specific sample_file_id or
        all sample files when sample_file_id is None.

        If mz_min and mz_max are provided, only the data within
        the mz range will be returned. Else, all data will be returned.

        Similarly, if t_min and t_max are provided, only the spectrum data
        within the time range will be returned for given mz-range values.

        :param sample_file_id: sample file id, defaults to None
        :type sample_file_id: str, optional
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
        :return: Spectrum data for the given sample file id
        :rtype: pd.DataFrame
        """

        self.cached_spectrum_params.update(
            {
                "mz_min": mz_min,
                "mz_max": mz_max,
                "t_min": t_min,
                "t_max": t_max,
                "sample_file_id": sample_file_id,
            }
        )
        if sample_file_id:
            if (
                sample_file_id
                not in self.match_samples[  # pylint: disable=E1101
                    "sample_file_id"
                ].unique()
            ):
                raise ValueError(f"Invalid sample file id: {sample_file_id}")
            return self.get_sample_spectrum()
        else:  # If no specific sample_file_id is provided, compute for all samples
            return self.get_all_sample_spectra()

    @pa.check_output(spectrum_schema)
    def get_all_sample_spectra(self) -> pd.DataFrame:
        """
        Compute the spectrum data for all samples.

        :return: Spectrum data for all samples
        :rtype: pd.DataFrame
        """
        spectrum_df = pd.concat(
            [
                self.get_spectrum_data(sample_file_id=sample_file_id)
                for sample_file_id in self.match_samples[  # pylint: disable=E1101
                    "sample_file_id"
                ]
            ]
        )
        # If in developer mode, validate the schema
        if MJW_DEV_MODE:
            return spectrum_schema.validate(spectrum_df)
        # If not in developer mode, process parser functions
        spectrum_df = add_column_for_filtering(spectrum_df)
        spectrum_df = set_unique_index(spectrum_df)
        spectrum_df = calculate_tic_norm_intensity_and_cumsum_tic_ratio(spectrum_df)

        return spectrum_df

    @pa.check_output(spectrum_schema)
    def get_sample_spectrum(self) -> pd.DataFrame:
        """Get the spectrum data for a specific sample file id."

        :return: spectrum data for sample
        :rtype: pd.DataFrame
        """
        # Columns to add from sample-level DF to spectrum-level DF
        cols_to_add = [
            "sample_batch_name",
            "sample_item_name",
            "filename",
            "filter_id",
            "sample_item_type",
            "datetime",
            "datetime_utc",
            "sample_item_id",
            "instrument",
            "tic",
        ]
        sample_file_id = self.cached_spectrum_params["sample_file_id"]
        mz_min = self.cached_spectrum_params["mz_min"]
        mz_max = self.cached_spectrum_params["mz_max"]
        t_min = self.cached_spectrum_params["t_min"]
        t_max = self.cached_spectrum_params["t_max"]
        # Collect sample-level data
        match_samples = self.match_samples  # pylint: disable=E1101
        # Collect spectrum data
        cached_spectrum = self.cached_samples_spectra.get(sample_file_id, None)
        # Check if the spectrum is already cached with the same parameters
        if cached_spectrum:
            cached_params = cached_spectrum.get("params", {})
            if (
                cached_params.get("mz_min") == mz_min
                and cached_params.get("mz_max") == mz_max
                and cached_params.get("t_min") == t_min
                and cached_params.get("t_max") == t_max
            ):
                return cached_spectrum["data"]
        # Subset match_samples to the specific sample_file_id and collect spectrum data
        match_samples_round = match_samples[
            match_samples["sample_file_id"] == sample_file_id
        ]
        sample_spectrum = (
            self.data_source.load_sample_file_spectrum(  # pylint: disable=E1101
                sample_file_id=sample_file_id,
                mz_min=mz_min,
                mz_max=mz_max,
                t_min=t_min,
                t_max=t_max,
            )
        )
        sample_spectrum_df = pd.DataFrame(
            {
                "intensity": sample_spectrum["intensity"],
                "mz": sample_spectrum["mz"],
                "unit": np.repeat(
                    sample_spectrum["intensity_unit"],
                    len(sample_spectrum["mz"]),
                ),
                "sample_file_id": np.repeat(sample_file_id, len(sample_spectrum["mz"])),
            }
        )
        # Collect needed information from match_samples to sample_spectrum_df
        for col in cols_to_add:
            sample_spectrum_df[col] = match_samples_round[col].unique().tolist()[0]
        # Cache the spectrum data with the parameters
        self.cached_samples_spectra[sample_file_id] = {
            "data": sample_spectrum_df,
            "params": self.cached_spectrum_params.copy(),
        }
        for key in self.cached_spectrum_params:
            self.cached_spectrum_params[key] = None
        # If in developer mode, validate the schema
        if MJW_DEV_MODE:
            return spectrum_schema.validate(sample_spectrum_df)
        sample_spectrum_df = add_column_for_filtering(sample_spectrum_df)
        sample_spectrum_df = set_unique_index(sample_spectrum_df)
        sample_spectrum_df = calculate_tic_norm_intensity_and_cumsum_tic_ratio(
            sample_spectrum_df
        )

        return sample_spectrum_df
