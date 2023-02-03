from src.subpubpy import Subscriber
from queue import Queue, LifoQueue, PriorityQueue, SimpleQueue
from unittest import TestCase


class Test_SubscriberInit(TestCase):

    channels_name = ['channel-c1', 'channel-c2']

    def test_with_defaults(self):
        subscriber = Subscriber()
        self.assertEqual(len(subscriber), 0)
        self.assertIsInstance(subscriber.channels, set)

    def test_with_channels_str_input(self):
        # with one channel
        subscriber = Subscriber(self.channels_name[0])
        self.assertEqual(len(subscriber), 1)
        self.assertIsInstance(subscriber.channels, set)

    def test_with_channels_list_input(self):
        subscriber = Subscriber(self.channels_name)
        self.assertEqual(len(subscriber), 2)
        self.assertIsInstance(subscriber.channels, set)

    def test_with_channels_set_input(self):
        subscriber = Subscriber(set(self.channels_name))
        self.assertEqual(len(subscriber), 2)
        self.assertIsInstance(subscriber.channels, set)

    def test_with_channels_invalid_input(self):
        with self.assertRaises(ValueError):
            Subscriber({'t1': self.channels_name})

    def test_with_q_Queue_input(self):
        self.assertIsNotNone(Subscriber(q=None))
        self.assertIsNotNone(Subscriber(q=Queue()))
        self.assertIsNotNone(Subscriber(q=LifoQueue()))
        self.assertIsNotNone(Subscriber(q=PriorityQueue()))

        with self.assertRaises(ValueError):
            # this is because SimpleQueue is not an instance of Queue
            Subscriber(q=SimpleQueue())

        with self.assertRaises(ValueError):
            Subscriber(q=list())


class Test_Subscriber(TestCase):
    messages_list = ['message-1', ['message-2', 'message-3'],  # str, list
                     {'message-4'}, {'key-1': 'message-5'}]  # set, dict
    channels_name = ['channel-c1', 'channel-c2']
    subscriber = Subscriber()

    def test_get_message(self):
        self.assertEqual(self.subscriber.is_empty(), True)
        self.subscriber.get_message()

    def test_notify(self):
        self.subscriber.notify(self.messages_list[0])
        self.assertEqual(self.subscriber.is_empty(), False)

    def test_add_channel(self):
        # string channel name.
        self.subscriber.add_channel(self.channels_name[0])
        self.assertEqual(len(self.subscriber.channels), 1)

        # check if channel name is unique and args as well.
        self.subscriber.add_channel(*self.channels_name)
        self.assertEqual(len(self.subscriber.channels), 2)

        with self.assertRaises(TypeError):
            self.subscriber.add_channel(self.channels_name)

        with self.assertRaises(ValueError):
            self.subscriber.add_channel()

    def test_remove_channel(self):
        # string channel name.
        self.subscriber.remove_channel(self.channels_name[0])
        self.assertEqual(len(self.subscriber.channels), 1)

        # check if channel name is unique and args as well.
        self.subscriber.remove_channel(*self.channels_name)
        self.assertEqual(len(self.subscriber.channels), 0)

        with self.assertRaises(TypeError):
            self.subscriber.remove_channel(self.channels_name)

        with self.assertRaises(ValueError):
            self.subscriber.remove_channel()
