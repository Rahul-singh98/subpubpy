from abc import ABC, abstractmethod
from typing import Any, Callable, Union, Set, AnyStr
from threading import Thread
import inspect
from .utils import custom_hook
import logging
import threading
from queue import Queue

threading.excepthook = custom_hook


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
        # def caller_function(handler: dict, event: str, payload: Any,
        #                     verbose: bool = True):
        subscribers_set: Set = self._handler.get(event)

        if subscribers_set:
            for subscr in subscribers_set:
                # print(f"Calling thread for {event} {payload}")
                subscr(event, payload)
                th = Thread(name=f"{event}", target=subscr,
                            args=(event, payload), daemon=True)
                th.start()

            if verbose:
                logging.info(f"[Publish] {event} [Payload] {payload}")

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

        required_args = 2

        if 'self' in args.args:
            required_args += 1

        if len(args.args) == required_args:
            if event not in self._handler:
                self._handler[event] = set()
            self._handler[event].add(callback)

            if verbose:
                logging.info('[Subscribe] {0} assigned to {1}'.format(
                    callback, event))
        else:
            raise TypeError("Callback require two arguments")

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


class AbstractSubscriber(ABC):

    def __init__(self, manager, channels: Set = None, q: Queue = None, default_queue_size=150):
        self.__manager = manager
        self.__init_channels(channels)
        self.__init_q(q, default_queue_size)

    def __init_q(self, q: Queue = None, default_queue_size=150):
        if not isinstance(q, Queue) and q is not None:
            raise ValueError(
                f"""{q} is an invalid Queue type.
                Please check https://docs.python.org/3/library/queue.html#queue-objects for reference.
                """)
        if not q:
            q = Queue(maxsize=default_queue_size)
        self.__q = q

    def __init_channels(self, channels: Set = None):
        if not channels:
            self.__channels = set()
        elif isinstance(channels, str):
            self.__channels = set([channels])
        elif isinstance(channels, list) or \
                isinstance(channels, set):
            self.__channels = set(channels)
        else:
            raise ValueError(f"{channels} not an instance of str, list, set")

    @abstractmethod
    def get_message(self, block: bool = False):
        if block:
            return self.__q.get()

        if self.__q.empty():
            return None
        return self.__q.get_nowait()

    @abstractmethod
    def listen(self):
        yield next(self)

    @abstractmethod
    def notify(self, message: AnyStr):
        self.__q.put(message)

    @abstractmethod
    def add_channel(self, *args):
        if len(args) == 0:
            raise ValueError('Require channel or channels to add_channel')
        for channel in args:
            if self.__manager:
                self.__manager.add(channel, self)
            self.__channels.add(channel)

    @abstractmethod
    def remove_channel(self, *args):
        if len(args) == 0:
            raise ValueError('Require channel or channels to remove_channel')
        for channel in args:
            if channel in self.__channels:
                if self.__manager:
                    self.__manager.remove(channel, self)
                self.__channels.remove(channel)
        if len(self) == 0:
            del self

    @property
    def channels(self):
        return self.__channels

    def is_empty(self):
        return self.__q.empty()

    def __len__(self):
        return len(self.__channels)

    def __iter__(self):
        return self

    def __next__(self):
        return self.__q.get()


class AbstractPublisher(ABC):

    def __init__(self, manager) -> None:
        self.__manager = manager

    @abstractmethod
    def publish(self, channel: AnyStr, message: AnyStr):
        if self.__manager:
            return self.__manager.publish(channel, message)
        raise TypeError(f"Manager is not defined yet.")


class AbstractChannel(ABC):

    def __init__(self, name: AnyStr):
        self.__subscribers = set()
        self.__init_name(name)

    def __init_name(self, name: AnyStr):
        if isinstance(name, AbstractChannel):
            self = eval(name)

        if not isinstance(name, str):
            raise ValueError(f"{name} should be a valid string.")
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: AnyStr):
        self.__name = value

    @abstractmethod
    def attach(self, subscriber: AbstractSubscriber):
        self.__subscribers.add(subscriber)

    @abstractmethod
    def detach(self, subscriber: AbstractSubscriber):
        if subscriber in self.__subscribers:
            self.__subscribers.remove(subscriber)

    @abstractmethod
    def on_message(self, message):
        for subscr in self.__subscribers:
            subscr.notify(message)


class AbstractChannelManager(ABC):
    __channels = dict()

    @abstractmethod
    def add(self, channel_name: AnyStr, subscriber: AbstractSubscriber):
        pass

    @abstractmethod
    def remove(self, channel_name: AnyStr, subscriber: AbstractSubscriber):
        pass

    @abstractmethod
    def publish(self, channel_name, msg):
        pass
