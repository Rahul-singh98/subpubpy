from src.subpubpy import ThreadSafeSubpub, ThreadSafeRegexSubpub
from unittest import TestCase, main
from unittest.mock import patch
from threading import Thread
import io


class TestThreadSafeSubpub(TestCase):

    def tearDown(self) -> None:
        return super().tearDown()

    def test_creation(self):
        threadsafe_subpub = ThreadSafeSubpub()
        self.assertIsNotNone(threadsafe_subpub)

    def test_multiple_create(self):
        threadsafe_subpub = ThreadSafeSubpub()
        threadsafe_subpub_2 = ThreadSafeSubpub()

        # test objects
        self.assertEqual(threadsafe_subpub, threadsafe_subpub_2)

        # test objects addresses
        self.assertEqual(id(threadsafe_subpub), id(threadsafe_subpub_2))

    def test_sub_callback_int(self):
        threadsafe_subpub = ThreadSafeSubpub()
        with self.assertRaises(TypeError):
            threadsafe_subpub.sub("test_sub_callback_int", 2)

    def test_sub_callback_lambda(self):
        threadsafe_subpub = ThreadSafeSubpub()

        with self.assertRaises(TypeError):
            threadsafe_subpub.sub("test_sub_callback_lambda", lambda x: None)

    def test_sub_callback_function_1_param(self):
        threadsafe_subpub = ThreadSafeSubpub()

        def func(par): ...

        with self.assertRaises(TypeError):
            threadsafe_subpub.sub("test_sub_callback_function_1_param", func)

    def test_sub_callback_function_1_default_param(self):
        threadsafe_subpub = ThreadSafeSubpub()

        def func(par=None): ...

        with self.assertRaises(TypeError):
            threadsafe_subpub.sub(
                "test_sub_callback_function_1_default_param", func())

    def test_sub_callback_pass(self):
        simple_pubsub = ThreadSafeSubpub()

        def func(par1, par2): ...
        simple_pubsub.sub("test_sub_callback_pass", func)

    def test_unsub_no_event_subscription(self):
        threadsafe_subpub = ThreadSafeSubpub()

        with self.assertRaises(ValueError):
            threadsafe_subpub.unsub("test_unsub_no_event_subscription", None)

    def test_unsub_no_callback_subscr(self):
        threadsafe_subpub = ThreadSafeSubpub()

        def func(*args, **kwargs): ...

        with self.assertRaises(ValueError):
            threadsafe_subpub.unsub("test_unsub_no_callback_subscr", func)

    def test_unsub_passed(self):
        threadsafe_subpub = ThreadSafeSubpub()

        def func(arg1, arg2): ...

        threadsafe_subpub.sub('test_unsub_passed', func)
        threadsafe_subpub.unsub("test_unsub_passed", func)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_publish_passed(self, mock_out):
        threadsafe_subpub = ThreadSafeSubpub()
        event = "test_publish_passed"
        payload = "payload_test"

        def func(event, payload):
            print(f"{event} {payload}")

        threadsafe_subpub.sub(event, func)
        threadsafe_subpub.pub(event, payload)

        self.assertEqual(mock_out.getvalue(), f"{event} {payload}\n"*4)


class Runner():

    def __init__(self):
        self.threads = {}
        self.thread_results = {}

    def add(self, target, name):
        self.threads[name] = Thread(target=self.run, args=[target, name])
        self.threads[name].start()

    def run(self, target, name):
        self.thread_results[name] = 'fail'
        target()
        self.thread_results[name] = 'pass'

    def check_result(self, name):
        self.threads[name].join()
        assert (self.thread_results[name] == 'pass')


class TestThreadSafeRegexSubpub(TestCase):

    def test_create(self):
        threadsaferegex_subpub = ThreadSafeRegexSubpub()
        self.assertIsNotNone(threadsaferegex_subpub)


runner = Runner()


class MyTests(TestCase):
    @classmethod
    def setUpClass(cls):
        def func1():
            raise Exception("Error")

        def func2():
            return

        # runner.add(func1, 'test_raise_err')
        runner.add(func2, 'test_no_err')

    # def test_raise_err(self):
    #     runner.check_result('test_raise_err')

    def test_no_err(self):
        runner.check_result('test_no_err')
