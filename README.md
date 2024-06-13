# EasyJsonPy
EasyJsonPy is a Python library for loading and managing languages ​​and settings in JSON format.

## Installation

To install EasyJsonPy, simply use the pip install command

```bash
pip install easyjsonpy
```

## Usage

### Simple use of language functions.
You need the language files in your project in their respective path

```py
from easyjsonpy import (
    load_language,
    load_languages,
    set_language,
    translate_message,
    get_current_language,
    get_languages
)

# Load a single language
load_language('en', 'path/to/en.json')

# Load multiple languages
languages = [
    {'name': 'en', 'path': 'path/to/en.json'},
    {'name': 'es', 'path': 'path/to/es.json'}
]
load_languages(languages)

# Set the current language
set_language('en')

# Translate a message
message = translate_message('greeting.hello')
print(message)  # Output: Hello (if the translation exists in en.json)

# Get the current language
current_language = get_current_language()
print(current_language)  # Output: en

# Get all loaded languages
loaded_languages = get_languages()
print(loaded_languages)  # Output: {'en': {...}, 'es': {...}}
```

### You can load the language in the main file and get the translations in other files.


#### main.py

```py
from easyjsonpy import load_language, set_language
from test import example_function

load_language('en', 'en.json')
set_language('en')
example_function()
```

##### test.py

```py
from easyjsonpy import translate_message

def example_function():
    print(translate_message('helloWorld'))  # Output: Hello World
    print(translate_message('messages.example'))  # Output: Example Message
```

#### en.json

```json
{
    "messages": {
        "example": "Example Message"
    },
    "helloWorld": "Hello World"
}
```

#### Complete documentation of language features [here](./docs/language.md)

### Simple use of settings functions.
You need the setting file in your project in their respective path

```py
from easyjsonpy import (
    load_configuration,
    load_configurations,
    get_config_value,
    set_config_value,
    get_configuration,
    get_configurations,
    remove_configuration,
    remove_all_configurations
)

# Load a single configuration
load_configuration('config1', 'path/to/config1.json')

# Load multiple configurations
configs = [
    {'name': 'config1', 'path': 'path/to/config1.json'},
    {'name': 'config2', 'path': 'path/to/config2.json'}
]
load_configurations(configs)

# Get a value from a configuration
value = get_config_value('some.key', 'config1')
print(f"Value from config1: {value}")

# Set a value in a configuration
set_config_value('some.key', 'new_value', 'config1')

# Verify the value was set
updated_value = get_config_value('some.key', 'config1')
print(f"Updated value from config1: {updated_value}")

# Get the loaded configuration
config = get_configuration('config1')
print(f"Loaded config1: {config}")

# Get all loaded configurations
all_configs = get_configurations()
print(f"All loaded configurations: {all_configs}")

# Remove a specific configuration
remove_configuration('config1')
print(f"Configurations after removing config1: {get_configurations()}")

# Remove all configurations
remove_all_configurations()
print(f"Configurations after removing all: {get_configurations()}")
```

### Like the language, you can load the configuration in your main file and in the modules get the configuration directly

#### main.py

```py
from easyjsonpy import load_configuration
from test import example_function

load_configuration('default', 'config.json')
load_configuration('anotherConfig', 'anotherConfig.json')
example_function()
```

##### test.py

```py
from easyjsonpy import get_config_value


def example_function():
    print(get_config_value('key1', 'default'))  # Output: 'defaultValue'
    print(get_config_value('key1'))  # Default config_name is 'default'. Output: 'defaultValue'
    print(get_config_value('key2', 'anotherConfig'))  # Output: 'anotherValue'
```

#### config.json

```json
{
    "key1": "defaultValue"
}
```

#### anotherConfig.json

```json
{
    "key2": "anotherValue"
}
```

#### Complete documentation of language features [here](./docs/settings.md)
