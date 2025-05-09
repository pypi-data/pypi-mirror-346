import logging
import os

# Singleton instance to ensure configuration is loaded once
_config_instance = None
logger = logging.getLogger(__name__)


class Config:
    def __init__(self, default_config_path):
        """
        Initialize the Config class.
        :param main_con
        fig_path: Path to the main YAML configuration file.
        """
        self.configs = {}
        self.commission_data = {}  # Preloaded commission data
        self.default_config_path = default_config_path
        self.custom_config_path = os.getenv("LIGHTQUANT_CONFIG_PATH", None)
        self.config_path = self.custom_config_path or self.default_config_path
        if self.config_path:
            self.base_dir = os.path.dirname(self.config_path)  # Base directory for relative paths
            self.load_config(self.config_path)

    def load_config(default_config_path):
        """
        Load the configuration globally.
        :param default_config_path: Path to the main configuration file.
        """
        global _config_instance
        if is_config_loaded():
            logger.info("Configuration is already loaded. Skipping reload.")
            return
        _config_instance = Config(default_config_path)
        logger.warn(f"Config loaded from file {_config_instance.config_path}")


# Global functions for managing configuration


def load_config(default_config_path):
    """
    Load the configuration globally.
    :param config_file_path: Path to the main configuration file.
    """
    global _config_instance
    _config_instance = Config(default_config_path)
    logger.warn(f"Config loaded from file {_config_instance.config_path}")


def is_config_loaded():
    """
    Check if the configuration is already loaded.
    :return: True if the configuration is loaded, otherwise False.
    """
    return _config_instance is not None


def get_config():
    """
    Retrieve the loaded configuration instance.
    :return: Config instance if loaded, otherwise raises ValueError.
    """
    if not is_config_loaded():
        raise ValueError("Configuration has not been loaded yet.")
    return _config_instance
