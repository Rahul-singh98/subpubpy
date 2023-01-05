from src.pubsubpy import SimplePubsub, ThreadSafePubSub, RegexPubsub, ThreadSafeRegexPubsub
from unittest import TestCase, main
from unittest.mock import patch
import io

class TestSimplePubsub(TestCase):

    def test_creation(self):
        s1 = SimplePubsub()

    def test_creation_multiple(self):
        s1 = SimplePubsub()
        s2 = SimplePubsub()

        # test instances
        self.assertNotEqual(s1, s2)

        # test instances id
        self.assertNotEqual(id(s1), id(s2))

    def test_sub_callback_int(self):
        s1 = SimplePubsub()
        with self.assertRaises(TypeError):
            s1.sub("test_event", 2)

    def test_sub_callback_lambda(self):
        s1 = SimplePubsub()
        s1.sub("test_event", lambda x: None)

    def test_sub_callback_function_1(self):
        s1 = SimplePubsub()

        def func(par):
            return None

        s1.sub("test_event", func)

    def test_sub_callback_function_2(self):
        s1 = SimplePubsub()

        def func(par=None):
            return None
        with self.assertRaises(TypeError):
            s1.sub("test_event", func())


# class TestThreadSafePubSub(TestCase):

#     def test_creation(self):
#         t1 = ThreadSafePubSub()

#     def test_multiple_create(self):
#         t1 = ThreadSafePubSub()
#         t2 = ThreadSafePubSub()

#         # test objects
#         self.assertEqual(t1, t2)

#         # test objects addresses
#         self.assertEqual(id(t1), id(t2))

#     def test_sub_callback_int(self):
#         s1 = ThreadSafePubSub()
#         with self.assertRaises(TypeError):
#             s1.sub("test_event", 2)

#     def test_sub_callback_lambda(self):
#         s1 = ThreadSafePubSub()
#         s1.sub("test_event", lambda x: None)

#     def test_sub_callback_function_1(self):
#         s1 = ThreadSafePubSub()

#         def func(par):
#             return None

#         s1.sub("test_event", func)

#     def test_sub_callback_function_2(self):
#         s1 = ThreadSafePubSub()

#         def func(par=None):
#             return None
#         with self.assertRaises(TypeError):
#             s1.sub("test_event", func())


class TestRegexPubsub(TestCase):

    def test_creation(self):
        t1 = RegexPubsub()

    def test_multiple_create(self):
        t1 = RegexPubsub()
        t2 = RegexPubsub()

        # test objects
        self.assertNotEqual(t1, t2)

        # test objects addresses
        self.assertNotEqual(id(t1), id(t2))

    def test_sub_callback_int(self):
        s1 = RegexPubsub()
        with self.assertRaises(TypeError):
            s1.sub("test_event", 2)

    def test_sub_callback_lambda(self):
        s1 = RegexPubsub()
        s1.sub("test_event", lambda x: None)

    def test_sub_callback_function_1(self):
        s1 = RegexPubsub()

        def func(par):
            return None

        s1.sub("test_event", func)

    def test_sub_callback_function_2(self):
        s1 = RegexPubsub()

        def func(par=None):
            return None
        with self.assertRaises(TypeError):
            s1.sub("test_event", func())


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_publisher_without_regex(self, mock_stdout):
        normal_val = "test_1234"
        t1 = RegexPubsub()

        def callback(_data):
            print(_data, end='')

        event_name = "test1"
        publish_msg = "okay"
        t1.sub(event_name, callback)

        t1.pub(event_name, publish_msg)
        self.assertEqual(
            mock_stdout.getvalue(),
            publish_msg
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_publisher_with_regex(self, mock_stdout):
        normal_val = "test_1234"
        t1 = RegexPubsub()

        def callback(_data):
            print(_data, end='')

        event_name = "test1"
        publish_msg = "okay"
        t1.sub(r"te.*", callback)

        t1.pub(event_name, publish_msg)
        self.assertEqual(
            mock_stdout.getvalue(),
            ""
        )


if __name__ == "__main__":
    main()
