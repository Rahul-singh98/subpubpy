# Subpubpy

## Motivation
At the time of creating high level application, programmers usually shares data between the instances.
Sometimes there are situations where we need to parse same data in multithreading or even multiprocessing, which is very tedious process. At that moments, subpubpy becomes a pioneer and works efficiently even for large applications.

## Description

* `pub`: Each classes have a method pub which refers to the term publish. So, pub is a method which is used to publish any message to the all subscribers events.

```python
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
```
`pub` requires two parameters, `event` name of the event and other is `payload` a message for all the subscribers. There is a third parameter `verbose` which is used to log [DEBUG] messages which is produced by the pub. If verbose is `False` means don't output log message else output message in logs.

* `sub`: Each classes have a method sub which referes to the term subscribe. So, sub is a method which is used to subscribe a event. 

```python
def sub(self, event: str, callback: Callable[[str, Any], None], verbose: bool = True) -> Union[
        None, TypeError]:
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
```
`sub` requires two parameters, `event` name of the event and other is `callback` a function which is called when some publishes a message which takes two parameters -> event, paylaod. There is a third parameter `verbose` which is used to log [DEBUG] messages which is produced by the pub. If verbose is `False` means don't output log message else output message in logs.


* `unsub`: Each classes have a method unsub which referes to the term unsubscribe. So, sub is a method which is used to unsubscribe a event. 

```python
def unsub(self, event: str, handler: Any, verbose: bool = True) -> Union[None, ValueError]:
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
```
`unsub` requires two parameters, `event` name of the event and other is `callback` a function which is called when some publishes a message which takes two parameters -> event, paylaod. There is a third parameter `verbose` which is used to log [DEBUG] messages which is produced by the pub. If verbose is `False` means don't output log message else output message in logs.


## API

### *SimpleSubpub*:
Simple publish subscriber model which works under the main thread.

### *ThreadSafeSubpub*:
Thread safe publish subscriber model which works under multithreading concept.

### *RegexSubpub*:
Publish subscriber model which works under the main thread with regular expressions.

### *ThreadSafeRegexSubpub*:
Thread safe publish subscriber model which works under multithreading concept and regular expression.


***If you find any issue please feel free to report that issue on [github](https://github.com/Rahul-singh98/subpubpy/issues)***