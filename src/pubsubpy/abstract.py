from abc import ABC, abstractmethod
from typing import Any, Callable, Union, List, AnyStr


class AbstractPubSub(ABC):
    """Absact pubsub class.

    Attributes:
    -----------
    _handler: dict
        dictionary data structure to handle key as event and value\n
        as the callable function which runs on when event is called.

    Methods:
    --------
    @abstractmethod\n
    pub(event, msg)
        event is published then notify everyone who have subscribed.

    @abstractmethod\n
    sub(event, callback)
        register callback with the event.
    """
    _handler = dict()

    def __init__(self):
        """Pubsub Base constructor
        """

    @abstractmethod
    def pub(self, event: str, payload: Any) -> None:
        """Publishes the events.

        Parameters:
        -----------
        event: str
            event which need to be published.

        payload: Any
            Any kind of data structure to handle with event.
        """
        pass

    @abstractmethod
    def sub(self, event: str, callback: Callable[[Any], None]) -> Union[None, TypeError]:
        """Subscribes event with callback.\n
        Here it checks if callback is not callable then raises TypeError \n
        else returns None.

        Parameters:
        -----------
        event: str
            event which need to be subscribe.

        callback: Callable
            callback must be callable function.
        """
        if not callable(callback):
            raise TypeError(f"{type(callback)} is not Callable")
        return None
