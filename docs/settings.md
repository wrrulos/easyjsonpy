### Load a Configuration
To load a configuration file, use the load_configuration function:

```py
from easyjsonpy import load_configuration, get_configuration

load_configuration('test', 'path/to/config.json')

# Get the loaded configuration
config = get_configuration('test')
print(config)
```

### Load Multiple Configurations
To load multiple configuration files, use the load_configurations function:

```py
from easyjsonpy import load_configurations, get_configurations

configs = [
    {'name': 'config1', 'path': 'path/to/config1.json'},
    {'name': 'config2', 'path': 'path/to/config2.json'}
]

load_configurations(configs)

# Get all loaded configurations
all_configs = get_configurations()
print(all_configs)
```

### Get a Configuration Value
To get a value from a configuration, use the get_config_value function:

```py
from easyjsonpy import get_config_value

value = get_config_value('some.key', 'config1')
print(value)
```

### Set a Configuration Value
To set a value in a configuration, use the set_config_value function:

```py
from easyjsonpy import set_config_value

set_config_value('some.key', 'new_value', 'config1')

# Verify the value was set
value = get_config_value('some.key', 'config1')
print(value)
```

### Load a Configuration Asynchronously
To asynchronously load a configuration file, use the async_load_configuration function:

```py
import asyncio
from easyjsonpy import async_load_configuration, get_configuration

async def main():
    await async_load_configuration('test', 'path/to/config.json')
    config = get_configuration('test')
    print(config)

asyncio.run(main())
```

### Load Multiple Configurations Asynchronously
To asynchronously load multiple configuration files, use the async_load_configurations function:

```py
import asyncio
from easyjsonpy import async_load_configurations, get_configurations

async def main():
    configs = [
        {'name': 'config1', 'path': 'path/to/config1.json'},
        {'name': 'config2', 'path': 'path/to/config2.json'}
    ]
    await async_load_configurations(configs)
    all_configs = get_configurations()
    print(all_configs)

asyncio.run(main())
```

### Set a Configuration Value Asynchronously
To asynchronously set a value in a configuration, use the async_set_config_value function:

```py
import asyncio
from easyjsonpy import async_load_configuration, async_set_config_value, get_config_value

async def main():
    await async_load_configuration('test', 'path/to/config.json')
    await async_set_config_value('some.key', 'new_value', 'test')
    value = get_config_value('some.key', 'test')
    print(value)

asyncio.run(main())
```

### Remove a specific Configuration
To remove a specific configuration, use the remove_configuration function:

```py
from easyjsonpy import remove_configuration, get_configurations

# Remove the configuration
remove_configuration('config1')

# Get all loaded configurations to verify
print(f"Configurations after removing config1: {get_configurations()}")
```

### Remove All Configurations
To remove all configurations, use the remove_all_configurations function:

```py
from easyjsonpy import remove_all_configurations, get_configurations

# Remove all configurations
remove_all_configurations()

# Get all loaded configurations to verify
print(f"Configurations after removing all: {get_configurations()}")
```