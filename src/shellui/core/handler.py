from ..common.types import Callable, List, Any, BaseElementInterface, EventUnit, KeyboardEvent
from ..common.debug import logging


class KeyboardManager:
    def __init__(self, parent: BaseElementInterface = None):
        """
        :param parent: Parent class object
        """
        self.parent: BaseElementInterface = parent or BaseElementInterface
        self.keyboard_events: List[KeyboardEvent] = []

    def add_keyboard_event(self, function: Callable, _lambda: Callable = lambda key_char: True) -> KeyboardEvent:
        event = KeyboardEvent(function, _lambda)
        self.keyboard_events.append(event)
        return event

    def key_pressed(self, key_char) -> List[Any]:
        return_list: List[Any] = []
        for event in self.keyboard_events:
            if event._lambda(key_char):
                logging.keyboard(f"CLASS <{self.parent.__class__.__name__}> (tag={self.parent.tag}) CALLS KEYBOARD EVENT <{event.function.__name__}> (agrs=None, kwargs=None)")
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
