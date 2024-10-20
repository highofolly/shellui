from ..common.types import Callable, List, Any, BaseElementInterface, EventUnit, KeyboardEvent, TypedDict
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
            if event.rule(key_char):
                logging.keyboard(f"CLASS <{self.parent.__class__.__name__}> (tag={self.parent.tag}) CALLS KEYBOARD EVENT <{event.function.__name__}> (agrs=None, kwargs=None)")
                return_list.append(event.function())
        return return_list


class FlagsManager(dict):
    def __init__(self, parent: BaseElementInterface):
        super(FlagsManager, self).__init__()
        self.parent: BaseElementInterface = parent or BaseElementInterface

    def set_flag(self, key: str, value: Any) -> None:
        self.__setattr__(key, value)

    def get_flag(self, key: str) -> bool:
        return self.__getattr__(key)

    def __getattr__(self, key) -> bool:
        flag = self.get(key, None)
        if flag is None:
            logging.warning(f"CLASS FLAG <{self.parent.__class__.__name__}> (tag={self.parent.tag}) <{key}> WAS NOT CREATED!")
        return flag

    def __setattr__(self, key: str, value: bool) -> None:
        if key in ["flags", "parent"]:
            super().__setattr__(key, value)
        else:
            if not isinstance(value, bool):
                raise TypeError(f"Expected type 'bool', got '{type(value)}' instead")
            self[key] = value


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
