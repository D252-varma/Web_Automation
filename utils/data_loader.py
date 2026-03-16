import json
import yaml
import os
from utils.logger import Logger

logger = Logger.get_logger()

class DataLoader:
    """Utility to load test data from JSON or YAML files."""

    @staticmethod
    def get_test_data(file_name):
        """Helper to find and load test data by name."""
        # Find path to 'data' directory relative to this file
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        file_path = os.path.join(data_dir, file_name)
        
        if file_name.endswith('.json'):
            return DataLoader.load_json(file_path)
        elif file_name.endswith('.yaml') or file_name.endswith('.yml'):
            return DataLoader.load_yaml(file_path)
        else:
            raise ValueError(f"Unsupported file format for: {file_name}")

    @staticmethod
    def load_json(file_path):
        if not os.path.exists(file_path):
            logger.error(f"Test data file not found: {file_path}")
            raise FileNotFoundError(f"Test data file not found: {file_path}")
        
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                logger.info(f"Successfully loaded JSON test data from: {file_path}")
                return data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON file {file_path}: {str(e)}")
                raise

    @staticmethod
    def load_yaml(file_path):
        if not os.path.exists(file_path):
            logger.error(f"Test data file not found: {file_path}")
            raise FileNotFoundError(f"Test data file not found: {file_path}")
        
        with open(file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                logger.info(f"Successfully loaded YAML test data from: {file_path}")
                return data
            except yaml.YAMLError as e:
                logger.error(f"Failed to parse YAML file {file_path}: {str(e)}")
                raise
