from src.subpubpy import Publisher
from unittest import TestCase


class Test_Publisher(TestCase):
    channel_name = 'channel-1'
    messages = 'msg-1'

    def test_init(self):
        self.assertIsNotNone(Publisher())

    def test_publish(self):
        publisher = Publisher()
        publisher.publish(self.channel_name, self.messages)

        # This produce nothing because manager is define in abstract class
        publisher.__manager = None
        publisher.publish(self.channel_name, self.messages)
