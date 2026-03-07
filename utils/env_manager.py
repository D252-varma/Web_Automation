import yaml
import os

class EnvironmentManager:
    """Utility to read environment configurations from config.yaml."""
    
    _config_data = None
    _env = None

    @classmethod
    def load_config(cls, config_path="config/config.yaml"):
        if cls._config_data is None:
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Config file not found: {config_path}")
            
            with open(config_path, "r") as file:
                yaml_data = yaml.safe_load(file)
                cls._env = yaml_data.get("environment", "dev")
                cls._config_data = yaml_data.get(cls._env, {})
                
                if not cls._config_data:
                    raise ValueError(f"Environment '{cls._env}' not found in {config_path}")

    @classmethod
    def get(cls, key, default=None):
        """Retrieve a specific configuration value."""
        if cls._config_data is None:
            cls.load_config()
        return cls._config_data.get(key, default)

    @classmethod
    def get_base_url(cls):
        return cls.get("base_url")

    @classmethod
    def is_headless(cls):
        return cls.get("headless", False)

    @classmethod
    def get_timeout(cls):
        return cls.get("timeout", 30000)
