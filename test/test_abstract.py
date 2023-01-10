from src.pubsubpy.abstract import AbstractPubSub
from unittest import TestCase, main


class TestAbstractPubSub(TestCase):

    def test_creation(self):
        with self.assertRaises(Exception):
            t1 = AbstractPubSub()


if __name__ == "__main__":
    main()
