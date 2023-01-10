from src.pubsubpy.utils import RegexDict
from unittest import TestCase, main


class TestRegexDict(TestCase):

    def test_creation(self):
        t1 = RegexDict()
        self.assertIsInstance(t1, dict)

    def test_simple_key(self):
        value = 'test'

        t1 = RegexDict()
        t1[value] = value
        self.assertEqual(t1.get(value), value)

    def test_regex_key_1(self):
        normal_val = "test_1234"
        t1 = RegexDict()

        t1[normal_val] = normal_val

        # Simple test
        self.assertEqual(t1.get(normal_val), normal_val)

        # Regex Test
        self.assertEqual(t1.get(r'test.*'), normal_val)
        self.assertEqual(t1[r'test.*'], normal_val)


if __name__ == "__main__":
    main()
