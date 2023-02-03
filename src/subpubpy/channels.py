from typing import AnyStr
from .abstract import AbstractSubscriber, AbstractChannel


class SimpleChannel(AbstractChannel):

    def __init__(self, name: AnyStr):
        super().__init__(name)

    def __str__(self) -> str:
        return "Channel {}".format(self.name)

    def __repr__(self) -> str:
        return "Channel({})".format(self.name)

    def attach(self, subscriber: AbstractSubscriber):
        return super().attach(subscriber)

    def detach(self, subscriber: AbstractSubscriber):
        return super().detach(subscriber)

    def on_message(self, message):
        return super().on_message(message)
