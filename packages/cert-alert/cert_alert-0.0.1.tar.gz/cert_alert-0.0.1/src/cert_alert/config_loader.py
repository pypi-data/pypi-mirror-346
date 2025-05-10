import logging  # For logging functionality
import yaml  # For YAML parsing
from pydantic import ValidationError  # For Exception handling

from cert_alert.models import Config  # Import Config model from local models module


class ConfigLoader:
    def __init__(self):
        # Initialize logger for this class
        self.logger = logging.getLogger(__name__)

    def read_config(self, config_path: str) -> Config:
        try:
            # Log the config file path being read
            self.logger.info(f"Reading config from {config_path}")
            
            # Open and read the YAML config file
            f = open(config_path, "r")
            data = yaml.safe_load(f)  # Parse YAML into Python dictionary
            f.close()

            # Validate the config data against the Config model using pydantic
            config = Config.model_validate(data)
            self.logger.info("✅ Config read successfully")
            self.logger.debug(f"⚙ Config loaded: {config.model_dump_json(indent=2)}")

            return config
        except ValidationError as e:
            # Handle pydantic validation errors
            message = f"❌ Config validation failed: {e}"
            self.logger.error(message)
            raise Exception(message)

        except FileNotFoundError:
            # Handle missing config file errors
            message = f"❌ ConfigFile {config_path} not found"
            self.logger.error(message)
            raise Exception(message)
