import pytest

from easyjsonpy import (
    load_configuration,
    async_load_configuration,
    load_configurations,
    async_load_configurations,
    get_configuration,
    get_configurations,
    get_config_value,
    async_set_config_value,
    set_config_value,
    remove_configuration,
    remove_all_configurations
)
from easyjsonpy.exceptions import (
    ConfigurationAlreadyLoadedError,
    ConfigurationNotLoadedError,
    ConfigurationFileNotFoundError,
)


CONFIG_PATH: str = "tests/config.json"
CONFIG_CONTENT: dict = {
    "test": "test",
    "tests": {
        "test1": "Test1"
    }
}


def test_no_configurations_loaded():
    """
    Test that no configurations are loaded
    """

    assert get_configurations() == {}


def test_configuration_not_loaded():
    """
    Test that a configuration is not loaded
    """

    with pytest.raises(ConfigurationNotLoadedError):
        get_configuration('test')


def test_load_configuration_not_found():
    """
    Test that loading a configuration that does not exist raises a ConfigurationFileNotFoundError
    """

    with pytest.raises(ConfigurationFileNotFoundError):
        load_configuration('test', 'notfound.json')


def test_load_configuration():
    """
    Test that a configuration is loaded
    """

    load_configuration('test', CONFIG_PATH)
    assert get_configuration('test') == CONFIG_CONTENT


def test_load_configuration_already_loaded():
    """
    Test that loading a configuration that is already loaded raises a ConfigurationAlreadyLoadedError
    """

    with pytest.raises(ConfigurationAlreadyLoadedError):
        load_configuration('test', CONFIG_PATH)


def test_set_config_value():
    """
    Test that a configuration value is set
    """

    set_config_value('test', 'test2', 'test')
    assert get_config_value('test2', 'test') == 'test2'

    # Reset the configuration value
    set_config_value('test', 'test', 'test')


def test_set_config_value_not_loaded():
    """
    Test that setting a configuration value that is not loaded raises a ConfigurationNotLoadedError
    """

    with pytest.raises(ConfigurationNotLoadedError):
        set_config_value('test', 'test', 'test2')


def test_get_config_value_not_loaded():
    """
    Test that getting a configuration value that is not loaded raises a ConfigurationNotLoadedError
    """

    with pytest.raises(ConfigurationNotLoadedError):
        get_config_value('test', 'test2')


def test_remove_configuration():
    """
    Test that a configuration is removed
    """

    remove_configuration('test')
    assert get_configurations() == {}


def test_remove_all_configurations():
    """
    Test that all configurations are removed
    """

    load_configuration('test', CONFIG_PATH)
    remove_all_configurations()
    assert get_configurations() == {}


def test_load_configurations():
    """
    Test that multiple configurations are loaded
    """

    load_configurations([
        {
            "name": "test",
            "path": CONFIG_PATH
        }
    ])

    assert get_configurations() == {
        "test": CONFIG_CONTENT
    }


@pytest.mark.asyncio
async def test_async_load_configuration():
    """
    Test that a configuration is loaded asynchronously
    """

    remove_all_configurations()
    await async_load_configuration('test', CONFIG_PATH)
    assert get_configuration('test') == CONFIG_CONTENT


@pytest.mark.asyncio
async def test_async_load_configurations():
    """
    Test that multiple configurations are loaded asynchronously
    """

    remove_all_configurations()
    await async_load_configurations([
        {
            "name": "test",
            "path": CONFIG_PATH
        }
    ])

    assert get_configurations() == {
        "test": CONFIG_CONTENT
    }


@pytest.mark.asyncio
async def test_async_set_config_value():
    """
    Test that a configuration value is set asynchronously
    """

    remove_all_configurations()
    await async_load_configuration('test', CONFIG_PATH)
    await async_set_config_value('test', 'test2', 'test')
    assert get_config_value('test2', 'test') == 'test2'

    # Reset the configuration value
    await async_set_config_value('test', 'test', 'test')