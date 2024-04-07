from data_processor import TestDrivingDataProcessor

config_path = "config.json"

if __name__ == "__main__":
    data_processor = TestDrivingDataProcessor(config_path)
    data_processor.process_files()
    data_processor.store_processed_data_as_csv()
