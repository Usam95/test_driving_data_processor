import json
from utils.logger import Logger
from utils.data_cleaner import DataCleaner
from utils.pydantic_models import TestDrivingData, Config
from typing import Optional, List, Dict
from pydantic import BaseModel, ValidationError
import os
import csv
import datetime


class TestDrivingDataProcessor:
    """
    Loads and processes the json files representing instances of the configured dataset.
    """
    def __init__(self, config_path: str):
        # Initialize configuration
        self.config = self.load_config(config_path)
        # Initialize logging
        logger_instance = Logger(self.config.logging_level)
        self.logger = logger_instance.logger  # Directly assign the logger attribute
        # Initialize class object for data cleaning
        self.data_cleaner = DataCleaner(self.config, self.logger)
        # Used to store the preprocessed dataset instances
        self.processed_data = []

    def load_config(self, config_path: str) -> Config:
        """
        Load and validate the program configuration.
        :param config_path:
        :return: instance of Config class with program configuration.
        """
        try:
            with open(config_path, 'r') as file:
                config_data = json.load(file)
                return Config(**config_data)
        except FileNotFoundError:
            print(f"Configuration file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the configuration file: {config_path}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while loading the config: {str(e)}")
            raise

    def load_and_validate_file(self, file_path: str) -> Optional[Dict]:
        """
        Loads, cleans and validates the json file consisting of dataset instance data.
        :param file_path: path to json file containing dataset instance
        :return: dictionary consisting the parsed, cleaned and validated dataset instance.
        """
        if self.config.clean_data:
            data = self.data_cleaner.process_json_file(file_path)
            # Validate data against the pydantic model
            if data and isinstance(data, dict):
                test_driving = TestDrivingData(**data)
                return test_driving.dict()
            else:
                return None
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # Validate data against the pydantic model
                    test_driving = TestDrivingData(**data)
                    return test_driving.dict()
            except FileNotFoundError as e:
                self.logger.error(f"File not found: {file_path}: {e}")
            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding JSON from {file_path}: {e}")
            except ValidationError as e:
                self.logger.error(f"Validation error for {file_path}: {e}")
            except Exception as e:
                self.logger.error(f"An unexpected error occurred with {file_path}: {e}")
            return None

    def process_files(self):
        """
        Processes all .json files in a given directory using the load_and_validate_file method.
        """
        for filename in os.listdir(self.config.dataset_path):
            file_path = os.path.join(self.config.dataset_path, filename)
            if os.path.isfile(file_path) and file_path.endswith('.json'):
                self.logger.info(f"Processing file: {file_path}")
                validated_json = self.load_and_validate_file(file_path)
                if validated_json is not None:
                    self.processed_data.append(validated_json)
                else:
                    self.logger.error(f"Failed to process file: {file_path}")

    def store_processed_data_as_csv(self):
        """
        Stores the processed data (list of dictionaries) in a csv file.
        """
        if not self.processed_data:
            self.logger.error("No processed data available to write to csv.")
            return
        # Create the name of resulting csv file consisting timestamp.
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv")
        output_filename = os.path.join(self.config.output_data_path, f"results_{timestamp}")
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Assuming all dictionaries have the same structure, use the keys of the first dictionary as headers
            #fieldnames = list(self.processed_data[0].keys())
            fieldnames = ["group_vehicle_number",  "record_country", "record_date", "comment", "total_driven_km"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for data in self.processed_data:
                writer.writerow(data)

        self.logger.info(f"Processed data has been stored in {output_filename}")
