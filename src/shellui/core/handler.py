from . import Callable, List, Any, dataclass
from .. import logging


@dataclass
class keyboardEvent:
    function: Callable
    _lambda: Callable


class KeyboardManager:
    def __init__(self, parent):
        """
        :param parent: Parent class object
        """
        self.parent: object = parent
        self.keyboard_events: List[keyboardEvent] = []

    def add_keyboard_event(self, function: Callable, _lambda: Callable = lambda key_char: True) -> keyboardEvent:
        event = keyboardEvent(function, _lambda)
        self.keyboard_events.append(event)
        return event

    def key_pressed(self, key_char) -> List[Any]:
        return_list: List[Any] = []
        for event in self.keyboard_events:
            if event._lambda(key_char):
                logging.keyboard(f"CLASS <{self.parent.__class__.__name__}> CALLS KEYBOARD EVENT <{event.function.__name__}> (agrs=None, kwargs=None)")
                return_list.append(event.function())
        return return_list


class FlagsManager:
    def __init__(self):
        self.flags = {}

    def __getattr__(self, item):
        return self.flags.get(item, None)

    def __setattr__(self, key, value: bool):
        if key == "flags":
            super().__setattr__(key, value)
        else:
            if not isinstance(value, bool):
                raise TypeError(f"Expected type 'bool', got '{type(value)}' instead")
            self.flags[key] = value

    def __delattr__(self, item):
        if item in self.flags:
            del self.flags[item]


class EventUnit:
    """
    Represents event unit that associated function with EventManager class
    """
    def __init__(self, parent):
        """
        :param parent: Parent class object
        """
        self.parent: object = parent

    def __setfunc__(self, func: Callable = None):
        """
        Sets the function for given event

        :param func: Function that will be called when the event is triggered
        """
        self.func: Callable = func

    def __call__(self, *args, **kwargs):
        """
        Calls function with the passed arguments

        :param args: Positional arguments that will be passed to function
        :param kwargs: Named arguments that will be passed to function
        """
        args_str = ', '.join(repr(arg) for arg in args[:2]) or None
        if len(args) > 2:
            args_str += ', ...'

        kwargs_items = list(kwargs.items())
        kwargs_str = ', '.join(f'{key}: {repr(value)}' for key, value in kwargs_items[:2]) or None
        if len(kwargs_items) > 2:
            kwargs_str += ', ...'

        logging.event(f"CLASS <{self.parent.__class__.__name__}> CALLS EVENT <{self.func.__name__}> (agrs={args_str}, kwargs={kwargs_str})")
        return self.func(*args, **kwargs)


class EventManager:
    """
    Manages creation and calling of events
    """
    def __init__(self, parent: object):
        """
        :param parent: Parent class object
        """
        class Create:
            """
            Responsible for creating events
            """
            def __init__(self, cls: EventManager):
                """
                :param cls: EventManager instance reference
                """
                self.cls = cls

            def __getattr__(self, name: str):
                """
                Creates an event by argument name

                :param name: Event argument name
                """
                return self.cls.call.__newattr__(name)

        class Call:
            """
            Responsible for calling events
            """
            def __newattr__(self, name: str):
                """
                Creates an EventUnit object for the specified event argument name

                :param name: Event argument name
                """
                setattr(self, name, EventUnit(parent))
                return getattr(self, name).__setfunc__

        self.create = Create(self)
        self.call = Call()
