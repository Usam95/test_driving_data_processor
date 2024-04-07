import json
import re
import os


class DataCleaner:
    """
    Cleans the instances in the dataset if configured in the config.json.
    Tries to fix invalid unicode sequences and add default values for the missing information.
    """
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def fix_invalid_unicode(self, input_str):
        """
        Detects and replaces invalid unicode sequences.
        """
        pattern = r'\\u[0-9a-fA-F]{0,2}[^0-9a-fA-F]+'
        return re.sub(pattern, '\ufffd', input_str)

    def convert_to_str(self, data):
        # Convert all values in the data dict to strings
        for key in data.keys():
            data[key] = str(data[key])
        return data

    def set_default_values(self, data):
        """
        Sets configured default values for instance attributes.
        """
        # Ensure 'group_vehicle_number' is present with a default value.
        data.setdefault('group_vehicle_number', self.config.default_group_vehicle_number)
        # Ensure 'group_vehicle_number' is present with a default value.
        data.setdefault('total_driven_km', self.config.default_total_driven_km)
        data.setdefault('record_country', self.config.default_record_country)
        data.setdefault('record_date', self.config.default_record_date)
        return data

    def process_json_file(self, file_path):
        """
        Reads a JSON file as a raw string, fixes invalid Unicode sequences,
        attempts to parse the corrected string into JSON, and writes the data back to the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_data = file.read()
            # Fix invalid Unicode sequences in the entire raw JSON string
            corrected_data = self.fix_invalid_unicode(raw_data)
            # Attempt to parse the corrected JSON string
            data = json.loads(corrected_data)
            # Ensure that only dictionaries are supported. E.g: skip data of type list.
            if isinstance(data, dict):
                # Set default values
                data = self.set_default_values(data)
                # Ensure all data are of string type
                data = self.convert_to_str(data)
                self.logger.info(f"Processed {file_path} successfully.")
                return data
            else:
                self.logger.error(f"Found a list instance: {file_path}.")
                return None
        except FileNotFoundError as e:
            self.logger.error(f"File not found: {file_path}: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {file_path}: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred with {file_path}: {e}")
        return None

    def clean_data(self):
        """
        Processes all .json files in the configured dataset folder.
        """
        for filename in os.listdir(self.config.dataset_path):
            file_path = os.path.join(self.config.dataset_path, filename)
            if os.path.isfile(file_path) and file_path.endswith('.json'):
                self.logger.info(f"Cleaning file: {file_path}")
                self.process_json_file(file_path)

