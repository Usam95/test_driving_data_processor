# Dataset Cleaner for Test Drive Metadata

## Project Overview
This project offers a solution to parse, validate, and clean the metadata of test drives. It considers common issues related to data validity, quality, and consistency. The dataset must be processed to ensure that the data are clean for further use.
The configuration of the processing is supported via a JSON file. The preprocessed data is stored in a CSV file, ready for further applications such as visualizations, machine learning model training etc. Details on any issues found during cleaning are stored in an appropriate `.log` file for analysis.

## Installation and Setup

### Setting Up the Virtual Environment with Conda

Before using the data cleaning generator, you must install certain libraries that are used as dependencies. These dependencies are listed in the `environment.yml` file and can be installed by creating a new virtual environment with Conda.

To create a Conda environment:

1. Open a terminal.
2. Navigate to the generator directory.
3. Run the command: `conda env create -f environment.yml`
4. This command sets up a new Conda environment named `dataset_cleaner_env` and installs all the necessary packages.

## Configuration

Configuration of the generator is done through a JSON config file, which is validated and parsed using the python Pydantic library.

### Configuration Parameters

- **`dataset_path`**: The path to the dataset folder containing the JSON files with metadata instances.
- **`output_data_path`**: Specifies the directory where the preprocessed data CSV file is stored.
- **`clean_data`**: A Boolean parameter that activates the cleaning of dataset instances.
- **`logging_level`**: Determines the level of logging output. The default level is set to `"error"`.

### Default Configuration Values

The following configuration elements are used as defaults values that used to initialize missing values during the data cleaning process:

- **`default_total_driven_km`**
- **`default_group_vehicle_number`**
- **`default_record_country`**
- **`default_record_date`**
