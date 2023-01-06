from .abstract import *
from .utils import RegexDict
from typing import List
from threading import Lock


class SimplePubsub(AbstractPubSub):
    """Simple publish subscriber model which works under the main\n
    thread.

    Attributes:
    -----------
    _handler: dict
        dictionary data structure to handle key as event and value\n
        as the callable function which runs on when event is called.

    Methods:
    --------
    pub(event, msg)
        event is published then notify everyone who have subscribed.

    sub(event, callback)
        register callback with the event."""

    def __init__(self):
        """Simple pubsub constructor."""
        super().__init__()

    def pub(self, event: str, payload: Any) -> None:
        """Publishes the events.

        Parameters:
        -----------
        event: str
            event which need to be published.

        payload: Any
            Any kind of data structure to handle with event.
        """
        subscribers: List = self._handler.get(event)

        if subscribers:
            for subscr in subscribers:
                if callable(subscr):
                    try:
                        subscr(payload)
                    except Exception as e:
                        print(e)

    def sub(self, event: str, callback: Callable[[Any], None]) -> Union[None, TypeError]:
        """Subscribes event with callback.\n
        It checks if callback is not callable then raises TypeError
        else returns None.
        Then, subscribes the event.

        Parameters:
        -----------
        event: str
            event which need to be subscribe.

        callback: Callable
            callback must be callable function.
        """

        super().sub(event, callback)

        if event not in self._handler:
            self._handler[event] = [callback]
        else:
            self._handler[event].append(callback)


class ThreadSafePubSub(AbstractPubSub):
    """Thread safe publish subscriber model which works under multithreading\n
    concept.

    Attributes:
    -----------
    _handler: dict
        dictionary data structure to handle key as event and value\n
        as the callable function which runs on when event is called.

    Methods:
    --------
    pub(event, msg)
        event is published then notify everyone who have subscribed.

    sub(event, callback)
        register callback with the event."""

    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if not cls._instance:
                cls._instance = super(ThreadSafePubSub, cls).__new__(cls)
        return cls._instance

    def pub(self, event: str, payload: Any) -> None:
        """Publishes the events.

        Parameters:
        -----------
        event: str
            event which need to be published.

        payload: Any
            Any kind of data structure to handle with event.
        """
        subscribers: List = self._handler.get(event)

        with self._lock:
            if subscribers:
                for subscr in subscribers:
                    if callable(subscr):
                        try:
                            subscr(payload)
                        except Exception as e:
                            print(e)

    def sub(self, event: str, callback: Callable[[Any], None]) -> Union[None, TypeError]:
        """Subscribes event with callback.\n
        It checks if callback is not callable then raises TypeError
        else returns None.
        Then, subscribes the event.

        Parameters:
        -----------
        event: str
            event which need to be subscribe.

        callback: Callable
            callback must be callable function.
        """

        super().sub(event, callback)

        # print("Sub Called")
        with self._lock:
            if event not in self._handler:
                self._handler[event] = [callback]
            else:
                self._handler[event].append(callback)


class RegexPubsub(AbstractPubSub):
    """Publish subscriber model which works under the main\n
    thread with regular expressions.

    Attributes:
    -----------
    _handler: RegexDict
        dictionary data structure to handle key as event and value\n
        as the callable function which runs on when event is called.

    Methods:
    --------
    pub(event, msg)
        event is published then notify everyone who have subscribed.

    sub(event, callback)
        register callback with the event."""

    def __init__(self):
        """Simple pubsub constructor."""
        self._handler = RegexDict()

    def pub(self, event: str, payload: Any) -> None:
        """Publishes the events.

        Parameters:
        -----------
        event: str
            event which need to be published.

        payload: Any
            Any kind of data structure to handle with event.
        """
        subscribers: List = self._handler.get(event)

        if subscribers:
            for subscr in subscribers:
                if callable(subscr):
                    try:
                        subscr(payload)
                    except Exception as e:
                        print(e)

    def sub(self, event: str, callback: Callable[[Any], None]) -> Union[None, TypeError]:
        """Subscribes event with callback.\n
        It checks if callback is not callable then raises TypeError
        else returns None.
        Then, subscribes the event.

        Parameters:
        -----------
        event: str
            event which need to be subscribe.

        callback: Callable
            callback must be callable function.
        """

        super().sub(event, callback)
        if self._handler.get(event):
            self._handler.get(event).append(callback)
        else:
            self._handler[event] = [callback]


class ThreadSafeRegexPubsub(ThreadSafePubSub):
    """Thread safe publish subscriber model which works under multithreading\n
    concept and regular expression.

    Attributes:
    -----------
    _handler: RegexDict
        dictionary data structure to handle key as event and value\n
        as the callable function which runs on when event is called.

    Methods:
    --------
    pub(event, msg)
        event is published then notify everyone who have subscribed.

    sub(event, callback)
        register callback with the event."""

    def __init__(self):
        self._handler = RegexDict()
