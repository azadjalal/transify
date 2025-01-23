
# Import relevant functions and classes from modules within the package
from .translator import load_languages, set_locale, get_locale, trans, lang

# List the names that should be exposed when using `from package import *`
__all__ = ['load_languages' , 'get_locale', 'set_locale', 'trans', 'lang']
