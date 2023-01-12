from src.subpubpy.utils import RegexDict
from unittest import TestCase, main


class TestRegexDict(TestCase):

    def test_creation(self):
        regex_dict = RegexDict()
        self.assertIsInstance(regex_dict, dict)

    def test_simple_key(self):
        param = 'test'

        regex_dict = RegexDict()
        regex_dict[param] = param
        self.assertEqual(regex_dict.get(param), param)

    def test_regex_key_1(self):
        param = "test_1234"
        regex_dict = RegexDict()

        regex_dict[param] = param

        # Simple test
        self.assertEqual(regex_dict.get(param), param)

        # Regex Test
        self.assertEqual(regex_dict.get(r'test.*'), param)
        self.assertEqual(regex_dict[r'test.*'], param)
