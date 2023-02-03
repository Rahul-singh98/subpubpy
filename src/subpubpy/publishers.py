from typing import AnyStr
from .abstract import AbstractPublisher
from .manager import _ChannelManager


class SimplePublisher(AbstractPublisher):

    def __init__(self) -> None:
        super().__init__(_ChannelManager())

    def publish(self, channel: AnyStr, message: AnyStr):
        return super().publish(channel, message)
