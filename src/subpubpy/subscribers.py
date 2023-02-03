from typing import AnyStr, Set
from queue import Queue
from .abstract import AbstractSubscriber
from .manager import _ChannelManager


class SimpleSubscriber(AbstractSubscriber):

    def __init__(self, channels: Set = None, q: Queue = None):
        super().__init__(_ChannelManager(), channels, q)

    def get_message(self, block: bool = False):
        return super().get_message(block)

    def listen(self):
        return super().listen()

    def notify(self, message: AnyStr):
        return super().notify(message)

    def add_channel(self, *args):
        return super().add_channel(*args)

    def remove_channel(self, *args):
        return super().remove_channel(*args)
