from abc import ABC, abstractmethod
from typing import Any, Callable, Union, List, AnyStr
from threading import Lock


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


class AbstractThreadSafe(object):
    """Utility class to convert base model in threadsafe model.
    """
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if not cls._instance:
                cls._instance = super(AbstractThreadSafe, cls).__new__(cls)
        return cls._instance


# class AbstractRegularExp(ABC):
#     """Utility class to integrate regular expression.

#     Methods:
#     --------

#     lookup(pattern, _from)
#         search for pattern in _from.
#     """

#     def lookup(self, pattern: str, _from: Union[List, AnyStr]) -> bool:
#         """Searches for the specific pattern in _from

#         Parameters:
#         -----------
#         pattern: str
#             pattern which we are looking for.

#         _from: Union[List, AnyStr]
#         """
#         if isinstance(_from, str):
#             pass
#         if isinstance(_from, list):
#             pass
#         return False
