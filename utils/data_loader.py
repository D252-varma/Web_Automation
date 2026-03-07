import json
import yaml
import os
from utils.logger import Logger

logger = Logger.get_logger()

class TestDataLoader:
    """Utility to load test data from JSON or YAML files."""

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
