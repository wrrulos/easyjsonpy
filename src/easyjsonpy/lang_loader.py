import json
import os
import aiofiles

from .exceptions import LanguageAlreadyLoadedError, LanguageNotLoadedError, LanguageFileNotFoundError

from typing import Union, Dict, Optional, List
from functools import reduce


class LangLoader:
    _instance: Optional['LangLoader'] = None
    languages: Dict[str, dict]
    language: Optional[str]

    def __new__(cls, *args, **kwargs) -> 'LangLoader':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.languages = {}
            cls._instance.language = None

        return cls._instance

    def load_language(self, lang_name: str, lang_path: Union[str, os.PathLike]) -> None:
        """
        Load a language file into the languages dictionary

        Args:
            lang_name (str): Language name
            lang_path (Union[str, os.PathLike]): Path to the language file

        Raises:
            LanguageAlreadyLoadedError: Language already loaded
            LanguageFileNotFoundError: Language file not found
        """

        if lang_name in self.languages:
            raise LanguageAlreadyLoadedError(f'Language {lang_name} already loaded')

        if not os.path.exists(lang_path):
            raise LanguageFileNotFoundError(f'Language file {lang_path} not found')

        with open(lang_path, 'r', encoding='utf-8') as lang_file:
            try:
                self.languages[lang_name] = json.load(lang_file)

            except json.decoder.JSONDecodeError:
                raise ValueError(f'Language file {lang_path} is not a valid JSON file')

    async def async_load_language(self, lang_name: str, lang_path: Union[str, os.PathLike]) -> None:
        """
        Asynchronously load a language file into the languages dictionary

        Args:
            lang_name (str): Language name
            lang_path (Union[str, os.PathLike]): Path to the language file

        Raises:
            LanguageAlreadyLoadedError: Language already loaded
            LanguageFileNotFoundError: Language file not found
        """
        if lang_name in self.languages:
            raise LanguageAlreadyLoadedError(f'Language {lang_name} already loaded')

        if not os.path.exists(lang_path):
            raise LanguageFileNotFoundError(f'Language file {lang_path} not found')

        async with aiofiles.open(lang_path, 'r', encoding='utf-8') as lang_file:
            content = await lang_file.read()

            try:
                self.languages[lang_name] = json.loads(content)

            except json.decoder.JSONDecodeError:
                raise ValueError(f'Language file {lang_path} is not a valid JSON file')

    def load_languages(self, languages: List[Dict[str, Union[str, os.PathLike]]]) -> None:
        """
        Load multiple language files into the languages dictionary

        Args:
            languages (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with language names and paths

        Raises:
            ValueError: If the input list or any of its elements is not correctly structured
        """

        self._check_language_list(languages=languages)

        for language in languages:
            self.load_language(language['name'], language['path'])

    async def async_load_languages(self, languages: List[Dict[str, Union[str, os.PathLike]]]) -> None:
        """
        Asynchronously load multiple language files into the languages dictionary

        Args:
            languages (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with language names and paths

        Raises:
            ValueError: If the input list or any of its elements is not correctly structured
        """

        self._check_language_list(languages=languages)

        for language in languages:
            await self.async_load_language(language['name'], language['path'])

    def set_language(self, lang_name: str) -> None:
        """
        Set the current language

        Args:
            lang_name (str): Language name

        Raises:
            LanguageNotLoadedError: Language not loaded
        """

        if lang_name not in self.languages:
            raise LanguageNotLoadedError(f'Language {lang_name} not loaded')

        self.language = lang_name

    def get_message(self, key: str) -> str:
        """
        Get the translation for a key

        Args:
            key (str): Translation key

        Returns:
            str: Translation
        """

        if self.language is None:
            raise LanguageNotLoadedError('Language not set')

        keys = key.split('.')
        return reduce(lambda d, k: d.get(k, key) if isinstance(d, dict) else key, keys, self.languages[self.language])

    def get_language(self) -> Optional[str]:
        """
        Get the current language

        Returns:
            Optional[str]: Current language
        """

        return self.language

    def get_languages(self) -> Dict[str, dict]:
        """
        Get the languages dictionary

        Returns:
            Dict[str, dict]: Languages dictionary
        """

        return self.languages

    def _check_language_list(self, languages: List[Dict[str, Union[str, os.PathLike]]]) -> None:
        """
        Check if the input list is correctly structured
        and raise an error if it is not.

        Args:
            languages (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with language names and paths

        Raises:
            ValueError: If the input list or any of its elements is not correctly structured
            ValueError:
            ValueError: _description_
            ValueError: _description_
        """

        if not isinstance(languages, list):
            raise ValueError('languages must be a list of dictionaries')

        for language in languages:
            if not isinstance(language, dict):
                raise ValueError('Each language entry must be a dictionary')

            if 'name' not in language or 'path' not in language:
                raise ValueError('Each language dictionary must have "name" and "path" keys')

            if not isinstance(language['name'], str) or not isinstance(language['path'], (str, os.PathLike)):
                raise ValueError('"name" must be a string and "path" must be a string or os.PathLike')


lang_loader = LangLoader()


def load_language(lang_name: str, lang_path: Union[str, os.PathLike]) -> None:
    """
    Load a language file into the languages dictionary

    Args:
        lang_name (str): Language name
        lang_path (Union[str, os.PathLike]): Path to the language file

    Raises:
        LanguageAlreadyLoadedError: Language already loaded
        LanguageFileNotFoundError: Language file not found
    """

    lang_loader.load_language(lang_name, lang_path)


def load_languages(languages: List[Dict[str, Union[str, os.PathLike]]]) -> None:
    """
    Load multiple language files into the languages dictionary

    Args:
        languages (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with language names and paths

    Raises:
        ValueError: If the input list or any of its elements is not correctly structured
    """

    lang_loader.load_languages(languages)


async def async_load_language(lang_name: str, lang_path: Union[str, os.PathLike]) -> None:
    """
    Asynchronously load a language file into the languages dictionary

    Args:
        lang_name (str): Language name
        lang_path (Union[str, os.PathLike]): Path to the language file

    Raises:
        LanguageAlreadyLoadedError: Language already loaded
        LanguageFileNotFoundError: Language file not found
    """

    await lang_loader.async_load_language(lang_name, lang_path)


async def async_load_languages(languages: List[Dict[str, Union[str, os.PathLike]]]) -> None:
    """
    Asynchronously load multiple language files into the languages dictionary

    Args:
        languages (List[Dict[str, Union[str, os.PathLike]]]): List of dictionaries with language names and paths

    Raises:
        ValueError: If the input list or any of its elements is not correctly structured
    """

    await lang_loader.async_load_languages(languages)


def set_language(lang_name: str) -> None:
    """
    Set the current language

    Args:
        lang_name (str): Language name

    Raises:
        LanguageNotLoadedError: Language not loaded
    """

    lang_loader.set_language(lang_name)


def get_current_language() -> Optional[str]:
    """
    Get the current language

    Returns:
        Optional[str]: Current language
    """

    return lang_loader.get_language()

def get_language(lang_name: str) -> Optional[dict]:
    """
    Get the language dictionary

    Args:
        lang_name (str): Language name

    Returns:
        Optional[dict]: Language dictionary
    """

    language: Union[dict, None] = lang_loader.get_languages().get(lang_name)

    if language is None:
        raise LanguageNotLoadedError(f'Language {lang_name} not loaded')

    return language

def get_languages() -> Dict[str, dict]:
    """
    Get the languages dictionary

    Returns:
        Dict[str, dict]: Languages dictionary
    """

    return lang_loader.get_languages()


def remove_language(lang_name: str) -> None:
    """
    Remove a language from the languages dictionary

    Args:
        lang_name (str): Language name
    """

    if not lang_loader.languages:
        raise LanguageNotLoadedError(f'Language {lang_name} not loaded')

    lang_loader.languages.pop(lang_name, None)


def remove_languages(lang_names: List[str]) -> None:
    """
    Remove multiple languages from the languages dictionary

    Args:
        lang_names (List[str]): List of language names
    """

    for lang_name in lang_names:
        remove_language(lang_name)


def remove_all_languages() -> None:
    """
    Remove all languages from the languages dictionary
    """

    lang_loader.languages = {}


def translate_message(key: str) -> str:
    """
    Get the translation for a key

    Args:
        key (str): Translation key

    Returns:
        str: Translation
    """

    return lang_loader.get_message(key)
