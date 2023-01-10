from abc import ABC, abstractmethod
from typing import Any, Callable, Union, List
import logging


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

    unsub(event, callback)
        unregister callback with the event.
    """
    _handler = dict()

    def __init__(self):
        """Pubsub Base constructor
        """

    @abstractmethod
    def pub(self, event: str, payload: Any, send_event: bool = False, verbose: bool = True) -> None:
        """Publishes the events.

        Parameters:
        -----------
        event: str
            event which need to be published.

        payload: Any
            Any kind of data structure to handle with event.

        send_event: bool
            publisher wants to send event name in callback or not.

        verbose: bool
            used for logging purpose if False no log message are passed.
        """
        subscribers: List = self._handler.get(event)

        if subscribers:
            for subscr in subscribers:
                if callable(subscr):
                    try:
                        subscr(payload) if event else subscr(event, payload)
                    except Exception as e:
                        logging.error(f"[Publish] {event} causing error {e}")
        if verbose:
            logging.info(f"[Publish] {event}\n [Payload] {payload}")

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

        verbose: bool
            used for logging purpose if False no log message are passed.
        """

        if not callable(callback):
            raise TypeError(f"{type(callback)} is not Callable")

        if event not in self._handler:
            self._handler[event] = [callback]
        else:
            self._handler[event].append(callback)

        if verbose:
            logging.info('[Subscribe] {0} assigned to {1}'.format(
                callback, event))
        return None

    def unsub(self, event: str, callback: Callable[[str, Any], None], verbose: bool = True) -> Union[
            None, TypeError, ValueError]:
        """Unsubscribes event with callback.\n
        Unsubscribe checks callback is assigned to event else raise ValueError.

        Parameters:
        -----------
        event: str
            event which need to be subscribe.

        callback: Callable
            callback must be callable function.

        verbose: bool
            used for logging purpose if False no log message are passed.
        """
        if not callable(callback):
            raise TypeError(f"{type(callback)} is not Callable")

        if event in self._handler:
            if callback in self._handler.get(event):
                idx = self._handler.get(event).index(callback)
                self._handler[event].remove(idx)

                if verbose:
                    logging.info('[Unubscribe] {0} assigned to {1}'.format(
                        callback, event))
                return None
        raise ValueError(f"{callback} is not subscribed with {event}")
