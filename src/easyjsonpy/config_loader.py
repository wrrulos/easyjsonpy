import json
import os
import aiofiles

from .exceptions import ConfigurationAlreadyLoadedError, ConfigurationFileNotFoundError, ConfigurationNotLoadedError

from typing import Union, Dict, Optional, List
from functools import reduce


class ConfigLoader:
    _instance: Optional['ConfigLoader'] = None
    configurations: Dict[str, dict]
    config_paths: Dict[str, str]

    def __new__(cls, *args, **kwargs) -> 'ConfigLoader':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.configurations = {}
            cls._instance.config_paths = {}

        return cls._instance

    def load_configuration(self, config_name: str, config_path: Union[str, os.PathLike]) -> None:
        """
        Load a configuration from a JSON file

        Args:
            config_name (str): Configuration name
            config_path (Union[str, os.PathLike]): Path to the configuration file

        Raises:
            ConfigurationAlreadyLoadedError: Configuration already loaded
            ConfigurationFileNotFoundError: Configuration file not found
            ValueError: Configuration file is not a valid JSON file
        """

        if config_name in self.configurations:
            raise ConfigurationAlreadyLoadedError(f'Configuration {config_name} already loaded')

        if not os.path.exists(config_path):
            raise ConfigurationFileNotFoundError(f'Configuration file {config_path} not found')

        with open(config_path, 'r', encoding='utf-8') as config_file:
            try:
                self.configurations[config_name] = json.load(config_file)
                self.config_paths[config_name] = config_path
            except json.decoder.JSONDecodeError:
                raise ValueError(f'Configuration file {config_path} is not a valid JSON file')

    async def async_load_configuration(self, config_name: str, config_path: Union[str, os.PathLike]) -> None:
        """
        Load a configuration from a JSON file asynchronously

        Args:
            config_name (str): Configuration name
            config_path (Union[str, os.PathLike]): Path to the configuration file

        Raises:
            ConfigurationAlreadyLoadedError: Configuration already loaded
            ConfigurationFileNotFoundError: Configuration file not found
            ValueError: Configuration file is not a valid JSON file
        """

        if config_name in self.configurations:
            raise ConfigurationAlreadyLoadedError(f'Configuration {config_name} already loaded')

        if not os.path.exists(config_path):
            raise ConfigurationFileNotFoundError(f'Configuration file {config_path} not found')

        async with aiofiles.open(config_path, 'r', encoding='utf-8') as config_file:
            content: str = await config_file.read()

            try:
                self.configurations[config_name] = json.loads(content)
                self.config_paths[config_name] = config_path

            except json.decoder.JSONDecodeError:
                raise ValueError(f'Configuration file {config_path} is not a valid JSON file')

    def load_configurations(self, configurations: List[Dict[str, Union[str, os.PathLike]]]) -> None:
        """
        Load multiple configurations from JSON files

        Args:
            configurations (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with configuration names and paths
        """

        self._check_configuration_list(configurations=configurations)

        for configuration in configurations:
            self.load_configuration(configuration['name'], configuration['path'])

    async def async_load_configurations(self, configurations: List[Dict[str, Union[str, os.PathLike]]]) -> None:
        """
        Load multiple configurations from JSON files asynchronously

        Args:
            configurations (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with configuration names and paths
        """

        self._check_configuration_list(configurations=configurations)

        for configuration in configurations:
            await self.async_load_configuration(configuration['name'], configuration['path'])

    def get_config(self, key: str, config_name: str) -> Union[str, int, float, bool, None, dict, list]:
        """
        Get a value from a configuration by key
        The key can be a nested key separated by dots (example: 'key1.key2.key3')

        Args:
            key (str): Key to get the value from
            config_name (str): Configuration name

        Raises:
            ConfigurationNotLoadedError: Configuration not loaded

        Returns:
            Union[str, int, float, bool, None, dict, list]: Value from the configuration
        """

        if config_name not in self.configurations:
            raise ConfigurationNotLoadedError(f'Configuration {config_name} not loaded')

        keys = key.split('.')
        return reduce(lambda d, k: d.get(k, key) if isinstance(d, dict) else key, keys, self.configurations[config_name])

    def set_config(self, key: str, value: Union[str, int, float, bool, None, dict, list], config_name: str) -> None:
        """
        Set a value in a configuration by key and save the changes to the configuration file

        Args:
            key (str): Key to set the value in
            value (Union[str, int, float, bool, None, dict, list]): Value to set
            config_name (str): Configuration name

        Raises:
            ConfigurationNotLoadedError: Configuration not loaded
        """

        if config_name not in self.configurations:
            raise ConfigurationNotLoadedError(f'Configuration {config_name} not loaded')

        key_parts: List[str] = key.split('.')
        config_dict: dict = self.configurations[config_name]

        for k in key_parts[:-1]:
            config_dict: dict = config_dict.setdefault(k, {})

        config_dict[key_parts[-1]] = value
        config_path: str = self.config_paths[config_name]

        with open(config_path, 'w', encoding='utf-8') as config_file:
            json.dump(self.configurations[config_name], config_file, indent=4)

    async def async_set_config(self, key: str, value: Union[str, int, float, bool, None, dict, list], config_name: str) -> None:
        """
        Set a value in a configuration by key and save the changes to the configuration file asynchronously

        Args:
            key (str): Key to set the value in
            value (Union[str, int, float, bool, None, dict, list]): Value to set
            config_name (str): Configuration name

        Raises:
            ConfigurationNotLoadedError: Configuration not loaded
        """

        if config_name not in self.configurations:
            raise ConfigurationNotLoadedError(f'Configuration {config_name} not loaded')

        key_parts = key.split('.')
        config_dict = self.configurations[config_name]

        for part in key_parts[:-1]:
            config_dict = config_dict.setdefault(part, {})

        config_dict[key_parts[-1]] = value
        config_path = self.config_paths[config_name]

        async with aiofiles.open(config_path, 'w', encoding='utf-8') as config_file:
            await config_file.write(json.dumps(self.configurations[config_name], indent=4))

    def get_configurations(self) -> Dict[str, dict]:
        """
        Get all loaded configurations

        Returns:
            Dict[str, dict]: Loaded configurations
        """

        return self.configurations

    def _check_configuration_list(self, configurations: List[Dict[str, Union[str, os.PathLike]]]) -> None:
        """
        Check if a list of configurations is valid

        Args:
            configurations (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with configuration names and paths

        Raises:
            ValueError: Configuration list is not valid
            ValueError: Configuration entry is not valid
            ValueError: Configuration dictionary is not valid
            ValueError: "name" must be a string and "path" must be a string or os.PathLike
        """

        if not isinstance(configurations, list):
            raise ValueError('configurations must be a list of dictionaries')

        for configuration in configurations:
            if not isinstance(configuration, dict):
                raise ValueError('Each configuration entry must be a dictionary')

            if 'name' not in configuration or 'path' not in configuration:
                raise ValueError('Each configuration dictionary must have "name" and "path" keys')

            if not isinstance(configuration['name'], str) or not isinstance(configuration['path'], (str, os.PathLike)):
                raise ValueError('"name" must be a string and "path" must be a string or os.PathLike')


config_loader = ConfigLoader()


def load_configuration(config_name: str, config_path: Union[str, os.PathLike]) -> None:
    """
    Load a configuration from a JSON file

    Args:
        config_name (str): Configuration name
        config_path (Union[str, os.PathLike]): Path to the configuration file
    """

    config_loader.load_configuration(config_name, config_path)


def load_configurations(configurations: List[Dict[str, Union[str, os.PathLike]]]) -> None:
    """
    Load multiple configurations from JSON files

    Args:
        configurations (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with configuration names and paths
    """

    config_loader.load_configurations(configurations)


async def async_load_configuration(config_name: str, config_path: Union[str, os.PathLike]) -> None:
    """
    Load a configuration from a JSON file asynchronously

    Args:
        config_name (str): Configuration name
        config_path (Union[str, os.PathLike]): Configuration path
    """

    await config_loader.async_load_configuration(config_name, config_path)


async def async_load_configurations(configurations: List[Dict[str, Union[str, os.PathLike]]]) -> None:
    """
    Load multiple configurations from JSON files asynchronously

    Args:
        configurations (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with configuration names and paths
    """

    await config_loader.async_load_configurations(configurations)


def get_configuration(config_name: str) -> dict:
    """
    Get a loaded configuration

    Args:
        config_name (str): Configuration name

    Raises:
        ConfigurationNotLoadedError: Configuration not loaded

    Returns:
        dict: Loaded configuration
    """

    if config_name not in config_loader.get_configurations():
        raise ConfigurationNotLoadedError(f'Configuration {config_name} not loaded')

    return config_loader.get_configurations()[config_name]


def get_configurations() -> Dict[str, dict]:
    """
    Get all loaded configurations

    Returns:
        Dict[str, dict]: Loaded configurations
    """

    return config_loader.get_configurations()


def get_config_value(key: str, config_name: str = 'default') -> Union[str, int, float, bool, None, dict, list]:
    """
    Get a value from a configuration by key

    Args:
        key (str): Key to get the value from
        config_name (str, optional): Configuration name. Defaults to 'default'.

    Returns:
        Union[str, int, float, bool, None, dict, list]: Value from the configuration
    """

    return config_loader.get_config(key, config_name)


def set_config_value(key: str, value: Union[str, int, float, bool, None, dict, list], config_name: str = 'default') -> None:
    """
    Set a value in a configuration by key and save the changes to the configuration file

    Args:
        key (str): Key to set the value in
        value (Union[str, int, float, bool, None, dict, list]): Value to set
        config_name (str, optional): Configuration name. Defaults to 'default'.
    """

    config_loader.set_config(key, value, config_name)

async def async_set_config_value(key: str, value: Union[str, int, float, bool, None, dict, list], config_name: str = 'default') -> None:
    """
    Set a value in a configuration by key and save the changes to the configuration file asynchronously

    Args:
        key (str): Key to set the value in
        value (Union[str, int, float, bool, None, dict, list]): Value to set
        config_name (str, optional): Configuration name. Defaults to 'default'.
    """

    await config_loader.async_set_config(key, value, config_name)


def remove_configuration(config_name: str) -> None:
    """
    Remove a loaded configuration

    Args:
        config_name (str): Configuration name
    """

    if config_name not in config_loader.get_configurations():
        raise ConfigurationNotLoadedError(f'Configuration {config_name} not loaded')

    del config_loader.get_configurations()[config_name]


def remove_all_configurations() -> None:
    """
    Remove all loaded configurations
    """

    config_loader.get_configurations().clear()
    config_loader.config_paths.clear()
