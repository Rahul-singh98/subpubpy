from src.pubsubpy.abstract import AbstractThreadSafe, AbstractPubSub
from unittest import TestCase, main


class TestAbstractThreadSafe(TestCase):

    def test_creation(self):
        t1 = AbstractThreadSafe()

    def test_multiple_create(self):
        t1 = AbstractThreadSafe()
        t2 = AbstractThreadSafe()

        # test objects
        self.assertEqual(t1, t2)

        # test objects addresses
        self.assertEqual(id(t1), id(t2))


class TestAbstractPubSub(TestCase):

    def test_creation(self):
        with self.assertRaises(Exception):
            t1 = AbstractPubSub()


if __name__ == "__main__":
    main()
