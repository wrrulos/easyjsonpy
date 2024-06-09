import os
import json
import pytest

from easyjsonpy import (
    load_language,
    async_load_language,
    load_languages,
    async_load_languages,
    set_language,
    get_current_language,
    get_language,
    get_languages,
    remove_language,
    remove_languages,
    remove_all_languages,
    translate_message,
)
from easyjsonpy.exceptions import (
    LanguageAlreadyLoadedError,
    LanguageNotLoadedError,
    LanguageFileNotFoundError,
)

EN_LANG_PATH: str = "tests/en.json"
EN_LANG_CONTENT: dict = {'test': 'test', 'tests': { 'test1': 'Test1' }}
ES_LANG_PATH: str = "tests/es.json"
ES_LANG_CONTENT: dict = {'test': 'prueba', 'tests': { 'test1': 'Prueba1' }}


def test_no_languages_loaded():
    """
    Test that no languages are loaded
    """
    assert get_languages() == {}


def test_language_not_loaded():
    """
    Test that a language is not loaded
    """

    with pytest.raises(LanguageNotLoadedError):
        get_language("en")


def test_load_language_not_found():
    """
    Test that loading a language that does not exist raises a LanguageFileNotFoundError
    """

    with pytest.raises(LanguageFileNotFoundError):
        load_language('en', 'notfound.json')


def test_load_language():
    """
    Test that a language is loaded
    """

    load_language('en', EN_LANG_PATH)
    assert get_languages() == {'en': EN_LANG_CONTENT}


def test_load_language_already_loaded():
    """
    Test that loading a language that is already loaded raises a LanguageAlreadyLoadedError
    """

    with pytest.raises(LanguageAlreadyLoadedError):
        load_language('en', EN_LANG_PATH)


def test_set_language():
    """
    Test that the current language is set
    """

    set_language('en')
    assert translate_message('test') == 'test'


def test_current_language():
    """
    Test that the current language is retrieved
    """

    assert get_current_language() == 'en'


def test_get_language():
    """
    Test that a language is retrieved
    """

    assert get_language('en') == EN_LANG_CONTENT


def test_remove_language():
    """
    Test that a language is removed
    """

    remove_language('en')
    assert get_languages() == {}


def test_load_languages():
    """
    Test that multiple languages are loaded
    """

    load_languages([
        {'name': 'en', 'path': EN_LANG_PATH},
        {'name': 'es', 'path': ES_LANG_PATH}
    ])

    assert get_languages() == {
        'en': EN_LANG_CONTENT,
        'es': ES_LANG_CONTENT,
    }


def test_remove_languages():
    """
    Test that multiple languages are removed
    """

    remove_languages(['en', 'es'])
    assert get_languages() == {}


def test_remove_all_languages():
    """
    Test that all languages are removed
    """

    load_languages([
        {'name': 'en', 'path': EN_LANG_PATH},
        {'name': 'es', 'path': ES_LANG_PATH}
    ])

    remove_all_languages()
    assert get_languages() == {}


def test_load_languages_already_loaded():
    """
    Test that loading multiple languages that are already loaded raises a LanguageAlreadyLoadedError
    """

    load_languages([
        {'name': 'en', 'path': EN_LANG_PATH},
        {'name': 'es', 'path': ES_LANG_PATH}
    ])

    with pytest.raises(LanguageAlreadyLoadedError):
        load_languages([
            {'name': 'en', 'path': EN_LANG_PATH},
            {'name': 'es', 'path': ES_LANG_PATH}
        ])


def test_translate_message():
    """
    Test that a message is translated
    """

    set_language('en')
    assert translate_message('test') == 'test'
    set_language('es')
    assert translate_message('test') == 'prueba'


@pytest.mark.asyncio
async def test_async_load_language():
    """
    Test that a language is loaded asynchronously
    """

    remove_all_languages()
    await async_load_language('en', EN_LANG_PATH)
    assert get_languages() == {'en': EN_LANG_CONTENT}


@pytest.mark.asyncio
async def test_async_load_languages():
    """
    Test that multiple languages are loaded asynchronously
    """

    remove_all_languages()
    await async_load_languages([
        {'name': 'en', 'path': EN_LANG_PATH},
        {'name': 'es', 'path': ES_LANG_PATH}
    ])

    assert get_languages() == {
        'en': EN_LANG_CONTENT,
        'es': ES_LANG_CONTENT,
    }
