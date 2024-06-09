### Load a Language
To load a language file, use the load_language function:

```py
from easyjsonpy import load_language

load_language('en', 'path/to/en.json')
```

### Load Multiple Languages
To load multiple language files, use the load_languages function:

```py
from easyjsonpy import load_languages

languages = [
    {'name': 'en', 'path': 'path/to/en.json'},
    {'name': 'es', 'path': 'path/to/es.json'}
]

load_languages(languages)
```

### Load a Language Asynchronously
To asynchronously load a language file, use the async_load_language function:

```py
import asyncio

from easyjsonpy import async_load_language

async def main():
    await async_load_language('en', 'test.json')


if __name__ == "__main__":
    asyncio.run(main())
```

### Load Multiple Languages Asynchronously
To asynchronously load multiple language files, use the async_load_languages function:

```py
import asyncio

from easyjsonpy import async_load_language

async def main():
    languages = [
        {'name': 'en', 'path': 'path/to/en.json'},
        {'name': 'es', 'path': 'path/to/es.json'}
    ]
    async_load_languages(languages)


if __name__ == "__main__":
    asyncio.run(main())
```

### Set the Current Language
To set the current language, use the set_language function:

```py
from easyjsonpy import set_language

set_language('en')
```

### Get the Translation of a Message
To get the translation of a message based on a key, use the translate_message function:

```py
from easyjsonpy import translate_message

message = translate_message('helloMessage')
other_message = translate_message('other.helloMessage')
print(message, other_message)
```

### Get the Current Language
To get the currently set language, use the get_current_language function:

```py
from easyjsonpy import get_current_language

current_language = get_current_language()
print(current_language)
```

### Get a Specific Language
To get the dictionary of a specific language, use the get_language function:

```py
from easyjsonpy import get_language

language = get_language('en')
print(language)
```

### Get All Loaded Languages
To get all loaded languages, use the get_languages function:


```py
from easyjsonpy import get_languages

languages = get_languages()
print(languages)
```

### Remove a Language
To remove a specific language, use the remove_language function:

```py
from easyjsonpy import remove_language

remove_language('en')
```

### Remove Multiple Languages
To remove multiple languages, use the remove_languages function:

```py
from easyjsonpy import remove_languages

remove_languages(['en', 'es'])
```

### Remove All Languages
To remove all loaded languages, use the remove_all_languages function:

```py
from easyjsonpy import remove_all_languages

remove_all_languages()
```