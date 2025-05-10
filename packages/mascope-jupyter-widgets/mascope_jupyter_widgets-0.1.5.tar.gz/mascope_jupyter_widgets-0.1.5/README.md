# Mascope Jupyter Widgets

This repository contains interactive widgets to construct data analysis notebooks for Mascope, utilizing [Mascope SDK](https://pypi.org/project/mascope_sdk/) to fetch data from the server.

All developer docs are in this document:

- **[🚀 Getting started](#getting-started)** - [installation](#installation) / [configuration](#mascope-url-configuration) / [authentication](#api-access-token-setup)
- **[📚 Modules](#modules)** - [filtering](#filtering) / [mascope_data](#mascope_data) / [mass_defect](#mass_defect) / [timeseries](#timeseries)

## Getting started

### Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management, and therefore it is a prerequisite for installation. Install `uv` following [their instructions](https://docs.astral.sh/uv/getting-started/installation/).

Once installed, open a terminal, navigate into the repository directory `mascope-jupyter-widgets/` and run

```sh
uv sync
```

### Environment configuration

**NOTE: The `.env` file needs to be placed in the directory from which you launch the notebooks**

To load data from the Mascope database, you will need to configure the URL as well as a personal access token.

1. In the source code directory, copy `.env.example` to a new file named `.env` in the same location.
2. Generate and copy a _Jupyter Notebooks_ access token in your Mascope account management.
3. Replace placeholders in the `.env` file with the URL of your Mascope instance and your personal access token:

```sh
MASCOPE_ACCESS_TOKEN=p3R5oN4l4cC35s70Ken
MASCOPE_URL="https://org.mascope.app"
```

**Note:** The `.env` file is gitignored to prevent accidental commit of personal access tokens. Never commit your actual token to the repository.

## Modules

The repository is structured into modules as follows:

```
mascope-jupyter-widgets/      Repository root
  mascope-jupyter-widgets/      Package directory
    filtering/                    Dataset filtering module
    mascope_data/                 Data loading module
    mass_defect/                  Mass defect analysis module
    timeseries/                   Timeseries analysis module
```

### `filtering/`

Module providing tools to select a subset of the loaded dataset based on various filtering criteria.

Names exported to package namespace:

- #### `FilteringWidget`

  Interactive notebook widget to filter a subset of the data currently loaded into [`MascopeDataWrapper`](#mascopedatawrapper). With the filters applied, all the data propertites exposed by `MascopeDataWrapper` return the filtered data.

### `mascope_data/`

Module providing tools to load and interface with Mascope data.

Names exported to package namespace:

- #### `MascopeDataBrowser`

  Interactive notebook widget to browse and load data from Mascope server.

- #### `MascopeDataWrapper`

  A class providing a standardized interface to the data loaded from Mascope, consisting of various [pandas](https://pandas.pydata.org/docs/index.html) dataframes exposed as class properties. An instance of the data wrapper is used as the input to analysis modules.

### `mass_defect/`

Module providing tools to perform mass defect analysis on the loaded dataset.

Names exported to package namespace:

- #### `MassDefectWidget`

  Interactive notebook widget to visualize the dataset based on mass defect, providing various ways of scaling and normalization.

### `spectrum/`

Module providing tools to perform spectrum analysis on the loaded dataset.

Names exported to package namespace:

- #### `SpectrumWidget`

  Interactive notebook widget to visualize the dataset spectrums.

### `timeseries/`

Module providing tools to perform timeseries analysis on the loaded dataset.

Names exported to package namespace:

- #### `TimeSeriesWidget`

  Interactive notebook widget to visualize the dataset based on time, providing various ways of aggregation.
