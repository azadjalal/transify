import os
import re
import json
import glob
import pathlib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Language:
    """
    Class to hold language translations.
    """
    path: str = 'lang'
    default_fallback: str = 'en'
    languages: dict = {}


# Instantiate the Language class
lang = Language()


def load_languages(path: str = 'lang', default_fallback: str = 'en'):
    """
    Load translations from JSON files located in the specified directory.
    """
    if path.startswith('/'):
        path = path[1:]
    lang.path = f'{os.getcwd()}/{path}'
    lang.default_fallback = default_fallback.lower()
    current_path = pathlib.Path(lang.path)
    if not (current_path.exists() and current_path.is_dir()):
        raise Exception(f"Error: Language directory {lang.path} does not exist.")
    logger.info(f'Loading language files from: {lang.path}')

    # Get list of language directories
    language_list = glob.glob(f'{lang.path}/*')
    try:
        for language in language_list:
            file_path = language.split('/')
            locale = file_path[-1].split('.')[0]  # Extract language code
            language_files = glob.glob(f'{lang.path}/{locale}/*.json')

            # Initialize dictionary for each language
            lang.languages[locale] = {}

            for file_path in language_files:
                with open(file=file_path, mode='r', encoding='utf8') as json_file:
                    file_name = file_path.split('/')[-1].split('.')[0]  # Extract file name
                    lang.languages[locale][file_name] = json.load(json_file)
    except Exception as ex:
        logger.error(f'Load languages failed: {ex}')


def get_locale() -> str:
    """
    Return the current language locale.
    """
    return lang.default_fallback


def set_locale(locale: str):
    """
    Change the current locale to a new language.

    Args:
        locale (str): The new locale (e.g., 'fa' for Persian).
    """
    load_languages(path=lang.path, default_fallback=locale.lower())


def trans(key: str, value: str = None):
    """
    Translate a key based on the current locale, supporting nested keys and dynamic replacements.

    Args:
        key (str): The translation key.
        value (str): Optional string for dynamic replacements.

    Returns:
        str: The translated string or the key if not found.
    """
    try:
        translated_value = _get_value(key)
        if isinstance(translated_value, str) and value:
            sub_keys_list = value.split('|')
            for sub_key in sub_keys_list:
                if ':' in sub_key:
                    values = sub_key.split(':')
                    for index, val in enumerate(values):
                        if re.search(r'(?<!\\)\.', val):
                            values[index] = _get_value(val)
                        else:
                            values[index] = re.sub(r'\\\.', '.', val)
                    translated_value = translated_value.replace(f':{values[0]}', values[1])
                elif '.' in sub_key:
                    sub_key_value = _get_value(sub_key)
                    if not translated_value.startswith(':attr'):
                        sub_key_value = sub_key_value.lower()
                    translated_value = translated_value.replace(':attr', sub_key_value)
                else:
                    translated_value = translated_value.replace(':attr', sub_key)
        return translated_value
    except KeyError:
        logger.error(f'Key `{key}` or its sub-keys are not correct.')
        return key


def _get_value(key: str, sub_key: str = None):
    """
    Retrieve the value for a given key, supporting nested keys.

    Args:
        key (str): The main translation key.
        sub_key (str, optional): An additional key for nested values.

    Returns:
        str: The translation value or the key if not found.
    """
    try:
        if sub_key is not None:
            key = f'{key.split(".")[0]}.{sub_key}'
        nested_names = key.split('.')
        value = lang.languages[get_locale()]
        for key_name in nested_names:
            value = value[key_name]
        return value
    except Exception as ex:
        logger.error(f'Key `{key}` not found: {ex}')
        return key
