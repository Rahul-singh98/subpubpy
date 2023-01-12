from src.subpubpy import SimpleSubpub, RegexSubpub
from unittest import TestCase, main
from unittest.mock import patch
import inspect
import io


class TestSimpleSubpub(TestCase):

    def tearDown(self) -> None:
        return super().tearDown()

    def test_creation(self):
        simple_subpub = SimpleSubpub()
        self.assertIsNotNone(simple_subpub)

    def test_creation_multiple(self):
        simple_subpub = SimpleSubpub()
        simple_subpub_2 = SimpleSubpub()

        # test instances
        self.assertNotEqual(simple_subpub, simple_subpub_2)

        # test instances id
        self.assertNotEqual(id(simple_subpub), id(simple_subpub_2))

    def test_sub_callback_int(self):
        simple_subpub = SimpleSubpub()
        with self.assertRaises(TypeError):
            simple_subpub.sub("test_sub_callback_int", 2)

    def test_sub_callback_lambda(self):
        simple_subpub = SimpleSubpub()

        with self.assertRaises(TypeError):
            simple_subpub.sub("test_sub_callback_lambda", lambda x: None)

    def test_sub_callback_function_1_param(self):
        simple_subpub = SimpleSubpub()

        def func(par): ...

        with self.assertRaises(TypeError):
            simple_subpub.sub("test_sub_callback_function_1_param", func)

    def test_sub_callback_function_1_default_param(self):
        simple_subpub = SimpleSubpub()

        def func(par=None): ...

        with self.assertRaises(TypeError):
            simple_subpub.sub(
                "test_sub_callback_function_1_default_param", func())

    def test_sub_callback_pass(self):
        simple_pubsub = SimpleSubpub()

        def func(par1, par2): ...
        simple_pubsub.sub("test_sub_callback_pass", func)

    def test_unsub_no_event_subscription(self):
        simple_subpub = SimpleSubpub()

        with self.assertRaises(ValueError):
            simple_subpub.unsub("test_unsub_no_event_subscription", None)

    def test_unsub_no_callback_subscr(self):
        simple_subpub = SimpleSubpub()

        def func(*args, **kwargs): ...

        with self.assertRaises(ValueError):
            simple_subpub.unsub("test_unsub_no_callback_subscr", func)

    def test_unsub_passed(self):
        simple_subpub = SimpleSubpub()

        def func(arg1, arg2): ...

        simple_subpub.sub('test_unsub_passed', func)
        simple_subpub.unsub("test_unsub_passed", func)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_publish_passed(self, mock_out):
        simple_subpub = SimpleSubpub()
        event = "test_publish_passed"
        payload = "payload_test"

        def func(event, payload):
            print(f"{event} {payload}")

        simple_subpub.sub(event, func)
        simple_subpub.pub(event, payload)

        self.assertEqual(mock_out.getvalue(), f"{event} {payload}\n")


class TestRegexSubpub(TestCase):

    def tearDown(self) -> None:
        return super().tearDown()

    def test_creation(self):
        regex_subpub = RegexSubpub()
        self.assertIsNotNone(regex_subpub)

    def test_creation_multiple(self):
        regex_subpub = RegexSubpub()
        regex_subpub_2 = RegexSubpub()

        # test instances
        self.assertNotEqual(regex_subpub, regex_subpub_2)

        # test instances id
        self.assertNotEqual(id(regex_subpub), id(regex_subpub_2))

    def test_sub_callback_int(self):
        regex_subpub = RegexSubpub()
        with self.assertRaises(TypeError):
            regex_subpub.sub("test_sub_callback_int", 2)

    def test_sub_callback_lambda(self):
        regex_subpub = RegexSubpub()

        with self.assertRaises(TypeError):
            regex_subpub.sub("test_sub_callback_lambda", lambda x: None)

    def test_sub_callback_function_1_param(self):
        regex_subpub = RegexSubpub()

        def func(par): ...
        with self.assertRaises(TypeError):
            regex_subpub.sub("test_sub_callback_function_1_param", func)

    def test_sub_callback_function_1_default_param(self):
        regex_subpub = RegexSubpub()

        def func(par=None): ...

        with self.assertRaises(TypeError):
            regex_subpub.sub(
                "test_sub_callback_function_1_default_param", func())

    def test_sub_callback_pass(self):
        regex_pubsub = RegexSubpub()

        def func(par1, par2): ...
        regex_pubsub.sub("test_sub_callback_pass", func)

    def test_unsub_no_event_subscription(self):
        regex_subpub = RegexSubpub()

        with self.assertRaises(ValueError):
            regex_subpub.unsub("test_unsub_no_event_subscription", None)

    def test_unsub_no_callback_subscr(self):
        regex_subpub = RegexSubpub()

        def func(*args, **kwargs): ...

        with self.assertRaises(ValueError):
            regex_subpub.unsub("test_unsub_no_callback_subscr", func)

    def test_unsub_passed(self):
        regex_subpub = RegexSubpub()

        def func(arg1, arg2): ...

        regex_subpub.sub('test_unsub_passed', func)
        regex_subpub.unsub("test_unsub_passed", func)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_publisher_without_regex(self, mock_stdout):
        regex_subpub = RegexSubpub()

        def callback(event, payload):
            print(f"{event} {payload}")

        event = "test_publisher_without_regex"
        payload = "okay"

        regex_subpub.sub(event, callback)
        regex_subpub.pub(event, payload)

        self.assertEqual(
            mock_stdout.getvalue(),
            f"{event} {payload}\n")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_publisher_with_regex(self, mock_stdout):
        regex_subpub = RegexSubpub()

        def callback(event, payload): ...
        # print(f"{event} {payload}")

        event = "test_publisher_with_regex"
        payload = "okay"
        regex_subpub.sub(r"te.*", callback)

        regex_subpub.pub(event, payload)
        self.assertEqual(mock_stdout.getvalue(), "")
