from ..common.types import Callable, List, Any, BaseElementInterface, EventUnit, KeyboardEvent, Collection, Union, Self
from ..common.debug import logger


class KeyboardHandler:
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

    def key_pressed(self, key) -> List[Any]:
        return_list: List[Any] = []
        for event in self.keyboard_events:
            if event.rule(key):
                logger.keyboard(f"CLASS <{self.parent.__class__.__name__}> (tag={self.parent.tag}) CALLS KEYBOARD EVENT <{event.function.__name__}> (agrs=None, kwargs=None)")
                return_list.append(event.function(key))
        return return_list


class FlagsController(dict):
    def __init__(self, parent: BaseElementInterface):
        super().__init__()
        self.parent: BaseElementInterface = parent or BaseElementInterface

    def set_flag(self, key: str, value: Any) -> None:
        self.__setattr__(key, value)

    def get_flag(self, key: str) -> bool:
        return self.__getattr__(key)

    def __getattr__(self, key) -> bool:
        flag = self.get(key, None)
        if flag is None:
            logger.warning(f"CLASS FLAG <{self.parent.__class__.__name__}> (tag={self.parent.tag}) <{key}> WAS NOT CREATED!")
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
        class Set:
            """
            Responsible for creating events
            """
            def __init__(self, cls: EventManager):
                """
                :param cls: EventManager instance reference
                """
                self.cls = cls

            def __getattr__(self, event_name: str):
                """
                Creates an event by argument name

                :param event_name: Event argument name
                """
                return self.cls.call.__newattr__(event_name)

        class Call:
            """
            Responsible for calling events
            """
            def __newattr__(self, event_name: str):
                """
                Creates an EventUnit object for the specified event argument name

                :param event_name: Event argument name
                """
                setattr(self, name, EventUnit(name, parent))
                return getattr(self, name).__setfunc__

        self.set = Set(self)
        self.call = Call()


class CursorController:
    def __init__(self, collection, position: int = 0, style: str = "> %(widget)s"):
        self.collection: Collection = collection
        self.__position: int = position
        self.style: str = style

    @property
    def current(self) -> BaseElementInterface:
        return self.get_element_by_position(self)

    @current.setter
    def current(self, link):  ...

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value: int):
        self.__position = value

    def get_element_by_position(self, position: Union[int, Self]) -> BaseElementInterface:
        if isinstance(position, self.__class__):
            position = position.position
        if len(self.collection) > position >= 0:
            return self.collection[position]

    def move(self, step: int, rule: Callable[[BaseElementInterface], bool]):
        while True:
            current = self.get_element_by_position(self.__position + step)
            if current:
                if rule(current):
                    self.__position += step
                    return self.__position
                else:
                    step += step
            else:
                return None
