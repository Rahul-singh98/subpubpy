from src.subpubpy.abstract import AbstractSubpub
from unittest import TestCase, main


class TestAbstractSubpub(TestCase):

    def test_creation(self):
        with self.assertRaises(Exception):
            t1 = AbstractSubpub()


if __name__ == "__main__":
    main()
