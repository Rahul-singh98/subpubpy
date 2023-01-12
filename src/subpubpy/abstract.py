from abc import ABC, abstractmethod
from typing import Any, Callable, Union, Set
from threading import Thread
import inspect
import logging


class AbstractSubpub(ABC):
    """Absact SubPub class.

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

    unsub(event, callback)
        unregister callback with the event.
    """
    _handler = dict()

    def __init__(self):
        """SubPub Base constructor
        """

    @abstractmethod
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
        def caller_function(handler: dict, event: str, payload: Any,
                            verbose: bool = True):
            subscribers_set: Set = handler.get(event)

            if subscribers_set:
                for subscr in subscribers_set:
                    subscr(event, payload)

                if verbose:
                    logging.info(f"[Publish] {event}\n [Payload] {payload}")

        th = Thread(target=caller_function, kwargs={
            'handler': self._handler,
            'event': event, 'payload': payload,
            "verbose": verbose})
        th.daemon = True
        th.start()

    @abstractmethod
    def sub(self, event: str, callback: Callable[[str, Any], None], verbose: bool = True) -> Union[None, TypeError]:
        """Subscribes event with callback.\n
        Here it checks if callback is not callable then raises TypeError \n
        else returns None.

        Parameters:
        -----------
        event: str
            event which need to be subscribe.

        callback: Callable
            callback must be callable function.

        verbose: Optional[bool]
            used for logging purpose if False no log message are passed.
        """

        if not callable(callback):
            raise TypeError(f"{type(callback)} is not Callable")

        args = inspect.getfullargspec(callback)

        if len(args.args) != 2:
            raise TypeError("Callback require two arguments")

        if event not in self._handler:
            self._handler[event] = set()
        self._handler[event].add(callback)

        if verbose:
            logging.info('[Subscribe] {0} assigned to {1}'.format(
                callback, event))

    def unsub(self, event: str, handler: Any, verbose: bool = True) -> Union[
            None, ValueError]:
        """Unsubscribes event with callback.\n
        Unsubscribe checks callback is assigned to event else raise ValueError.

        Parameters:
        -----------
        event: str
            event which need to be subscribe.

        hanlder: Any
            remove handler from the system.

        verbose: Optional[bool]
            used for logging purpose if False no log message are passed.
        """
        if event in self._handler:
            if handler in self._handler[event]:
                self._handler[event].remove(handler)

                if verbose:
                    logging.info('[Unubscribe] {0} assigned to {1}'.format(
                        handler, event))
                return
        raise ValueError(f"{handler} is not subscribed with {event}")
