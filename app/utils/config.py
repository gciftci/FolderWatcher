''' app/utils/config.py '''
# Third party imports
import configparser
import os
from typing import Any, Optional, List

# Local imports


class Config:
    """
    A Singleton-Class that monitors a folder for new files and processes them using a list of
    processes.
    """
    _instance: Optional['Config'] = None
    def __new__(cls) -> 'Config':
        """
        Ensures that only one instance of the Config class is created.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """
        Initializes the Config object by reading the config.ini file.
        """
        config_path = os.path.join(os.getcwd(), "config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(config_path)

    def get(self, section: str, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves the value of a specific key from a given section in the configuration.

        Args:
            section (str): The section name in the configuration file.
            key (str): The key name in the specified section.
            default (Optional[Any]): The default value to return if the key is not found.

        Returns:
            Any: The value associated with the key or the default value if the key is not found.
        """
        try:
            return self._config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def set(self, section: str, key: str, value: Any) -> None:
        """
        Sets the value of a specific key in a given section in the configuration.
        If the section does not exist, it will be created.

        Args:
            section (str): The section name in the configuration file.
            key (str): The key name in the specified section.
            value (Any): The value to set for the specified key.
        """
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, key, value)

_C = Config()
