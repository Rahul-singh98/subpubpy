from typing import AnyStr
from threading import Lock
from .abstract import AbstractSubscriber, AbstractChannel, AbstractChannelManager
from .channels import SimpleChannel


class _ChannelManager(AbstractChannelManager):
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(_ChannelManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__channels = dict()

    def _get_or_create(self, channel_name: AnyStr) -> AbstractChannel:
        if channel_name not in self.__channels:
            self.__channels[channel_name] = SimpleChannel(channel_name)
        return self.__channels[channel_name]

    def add(self, channel_name: AnyStr, subscriber: AbstractSubscriber):
        channel = self._get_or_create(channel_name)
        channel.attach(subscriber)

    def remove(self, channel_name: AnyStr, subscriber: AbstractSubscriber):
        channel = self._get_or_create(channel_name)
        channel.detach(subscriber)

    def publish(self, channel_name, msg):
        channel = self._get_or_create(channel_name)
        channel.on_message(msg)
