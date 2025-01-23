import unittest

from transify import *


class TestTranslation(unittest.TestCase):

    def setUp(self):
        # Set up any necessary environment variables or initial states
        load_languages(path="tests/lang", default_fallback="en")

    def test_1_load_languages(self):
        # Test if languages are loaded correctly
        self.assertIn('en', lang.languages)
        self.assertIn('fa', lang.languages)

    def test_2_set_locale(self):
        # Test setting a new locale
        set_locale(locale='fa')
        self.assertEqual(get_locale(), 'fa')
        set_locale(locale='en')

    def test_3_trans_basic(self):
        # Basic translation test
        self.assertEqual(trans(key='captions.hello'), 'Hello')
        self.assertEqual(trans(key='captions.goodbye'), 'Goodbye')

    def test_4_trans_with_sub_keys(self):
        # Test translation with sub keys
        self.assertEqual(
            trans(key='validations.between', value='score|min:1|max:20'),
            'The score must be between 1 and 20 values.'
        )
        self.assertEqual(
            trans(key='validations.between', value='captions.good_score|min:17|max:20'),
            'The good score must be between 17 and 20 values.'
        )
        self.assertEqual(
            trans(key='validations.required', value='username'),
            'The username is required.'
        )
        self.assertEqual(
            trans(key='validations.required', value='captions.first_name'),
            'The first name is required.'
        )

    def test_5_trans_nonexistent_key(self):
        # Testing a translation for a key that doesn't exist
        non_existent_key = 'messages.nonexistent'
        self.assertEqual(trans(key=non_existent_key), non_existent_key)

    def test_6_nested_keys(self):
        # Test translation in a different locale
        self.assertEqual(trans(key='messages.errors.user.not_found'), 'The user not found.')

    def test_7_trans_with_dot_in_key(self):
        # Test translation in a dot in key
        self.assertEqual(
            trans(key='messages.welcome', value='name:Azadjalal|website:azadjalal\\.ir'),
            'Welcome, Azadjalal to my website azadjalal.ir.')

    def test_8_trans_with_locale(self):
        # Test translation in a different locale
        set_locale(locale='fa')
        self.assertEqual(trans(key='captions.hello'), 'سلام')


if __name__ == '__main__':
    unittest.main()
