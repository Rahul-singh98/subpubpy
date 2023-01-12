from .abstract import *
from .utils import RegexDict
from threading import Lock


class SimpleSubpub(AbstractSubpub):
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
        register callback with the event.

    unsub(event, callback)
        unregister callback with the event."""

    def __init__(self):
        """Simple subpub constructor."""
        super().__init__()

    def pub(self, event: str, payload: Any, verbose: bool = True) -> None:
        """Publishes the events.

        Parameters:
        -----------
        event: str
            event which need to be published.

        payload: Any
            Any kind of data structure to handle with event.

        verbose: Optional[bool]
            used for logging purpose if False no log message are passed.
        """
        super().pub(event, payload, verbose)

    def sub(self, event: str, callback: Callable[[str, Any], None], verbose: bool = True) -> Union[None, TypeError]:
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

        verbose: Optional[bool]
            used for logging purpose if False no log message are passed.
        """

        super().sub(event, callback)


class ThreadSafeSubpub(AbstractSubpub):
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
        register callback with the event.

    unsub(event, callback)
        unregister callback with the event."""

    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if not cls._instance:
                cls._instance = super(ThreadSafeSubpub, cls).__new__(cls)
        return cls._instance

    def pub(self, event: str, payload: Any, verbose: bool = True) -> None:
        """Publishes the events.

        Parameters:
        -----------
        event: str
            event which need to be published.

        payload: Any
            Any kind of data structure to handle with event.

        verbose: Optional[bool]
            used for logging purpose if False no log message are passed.
        """
        with self._lock:
            super().pub(event, payload, verbose)

    def sub(self, event: str, callback: Callable[[str, Any], None], verbose: bool = True) -> Union[None, TypeError]:
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

        verbose: Optional[bool]
            used for logging purpose if False no log message are passed.
        """
        with self._lock:
            super().sub(event, callback, verbose)


class RegexSubpub(AbstractSubpub):
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
        register callback with the event.

    unsub(event, callback)
        unregister callback with the event."""

    def __init__(self):
        """Regex subpub constructor."""
        self._handler = RegexDict()

    def pub(self, event: str, payload: Any, verbose: bool = True) -> None:
        """Publishes the events.

        Parameters:
        -----------
        event: str
            event which need to be published.

        payload: Any
            Any kind of data structure to handle with event.

        verbose: Optional[bool]
            used for logging purpose if False no log message are passed.
        """
        super().pub(event, payload, verbose)

    def sub(self, event: str, callback: Callable[[str, Any], None], verbose: bool = True) -> Union[None, TypeError]:
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

        verbose: Optional[bool]
            used for logging purpose if False no log message are passed.
        """

        super().sub(event, callback)


class ThreadSafeRegexSubpub(ThreadSafeSubpub):
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
        register callback with the event.

    unsub(event, callback)
        unregister callback with the event."""

    def __init__(self):
        self._handler = RegexDict()
