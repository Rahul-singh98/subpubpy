from src.pubsubpy import ThreadSafePubSub
from unittest import TestCase, main
from unittest.mock import patch
from threading import Thread
import io


class TestThreadSafePubSub(TestCase):

    def test_creation(self):
        t1 = ThreadSafePubSub()

    def test_multiple_create(self):
        t1 = ThreadSafePubSub()
        t2 = ThreadSafePubSub()

        # test objects
        self.assertEqual(t1, t2)

        # test objects addresses
        self.assertEqual(id(t1), id(t2))

    def test_sub_callback_int(self):
        s1 = ThreadSafePubSub()
        with self.assertRaises(TypeError):
            s1.sub("test_event", 2)

    def test_sub_callback_lambda(self):
        s1 = ThreadSafePubSub()
        s1.sub("test_event", lambda x: None)

    def test_sub_callback_function_1(self):
        s1 = ThreadSafePubSub()

        def func(par):
            return None

        s1.sub("test_event", func)

    def test_sub_callback_function_2(self):
        s1 = ThreadSafePubSub()

        def func(par=None):
            return None
        with self.assertRaises(TypeError):
            s1.sub("test_event", func())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_publisher_1(self, mock_stdout):
        t1 = ThreadSafePubSub()

        def callback(_data):
            print(_data, end='')

        event_name = "test_event"
        publish_msg = "hello test"
        t1.sub(event_name, callback)

        t1.pub(event_name, publish_msg)
        self.assertEqual(
            mock_stdout.getvalue(),
            publish_msg
        )


class Runner():

    def __init__(self):
        self.threads = {}
        self.thread_results = {}

    def add(self, target, name):
        self.threads[name] = Thread(target = self.run, args = [target, name])
        self.threads[name].start()

    def run(self, target, name):
        self.thread_results[name] = 'fail'
        target()
        self.thread_results[name] = 'pass'

    def check_result(self, name):
        self.threads[name].join()
        assert(self.thread_results[name] == 'pass')


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

if __name__ == "__main__":
    main()
