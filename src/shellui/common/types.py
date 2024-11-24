from .interfaces import BaseElementInterface
from .debug import logger
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import *
from enum import Enum


class ElementState(Enum):
    """
    Enum representing the state of an element.

    :param MISSED: Indicates that the element was missed
    :type MISSED: int
    :param SELECTED: Indicates that the element was selected
    :type SELECTED: int
    """

    MISSED      = 0
    SELECTED    = 1


@dataclass
class Dimensions(ABC):
    """
    Represent abstract base class of dimensions with basic arithmetic operations.
    """

    def __iter__(self):
        yield self._x
        yield self._y

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self._x + other._x, self._y + other._y)
        elif isinstance(other, (int, float)):
            return self.__class__(self._x + other, self._y + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self._x - other._x, self._y - other._y)
        elif isinstance(other, (int, float)):
            return self.__class__(self._x - other, self._y - other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self._x * other, self._y * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self._x / other, self._y / other)
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self._x // other, self._y // other)
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self._x % other, self._y % other)
        return NotImplemented

    def __neg__(self):
        return self.__class__(-self._x, -self._y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._x == other._x and self._y == other._y
        return NotImplemented


@dataclass
class Position(Dimensions):
    """
    Represents a position in a 2D space.

    :param x: X-coordinate of the position.
    :type x: int
    :param y: Y-coordinate of the position.
    :type y: int
    """
    x: int
    y: int

    @property
    def _x(self):
        return self.x

    @property
    def _y(self):
        return self.y


@dataclass
class Size(Dimensions):
    """
    Represents the size with width and height.

    :param width: Width dimension.
    :type width: int
    :param height: Height dimension.
    :type height: int
    """
    width: int
    height: int

    @property
    def _x(self):
        return self.width

    @property
    def _y(self):
        return self.height


@dataclass
class KeyboardEvent:
    """
    Represents a keyboard event.

    :param function: The function to be executed on the event.
    :type function: typing.Callable[[], typing.Any]
    :param rule: Condition function for filtering elements
    :type rule: typing.Callable[[int], bool]
    """

    function: Callable[[], Any]
    rule: Callable[[int], bool]


@dataclass
class EventUnit:
    """
    Represents event unit that associated function with EventManager class
    """
    event_name: str
    parent: BaseElementInterface
    """Parent class object"""

    def __setfunc__(self, function: Callable = None):
        """
        Sets function for given event.

        :param function: Function that will be called when the event is triggered
        :type function: Callable
        """
        self.function: Callable = function

    def __call__(self, *args, **kwargs):
        """
        Calls function with the passed arguments.

        :param args: Positional arguments that will be passed to function
        :type args: typing.List
        :param kwargs: Named arguments that will be passed to function
        :type kwargs: typing.Dict
        """
        args_str = ', '.join(repr(arg) for arg in args[:2]) or None
        if len(args) > 2:
            args_str += ', ...'

        kwargs_items = list(kwargs.items())
        kwargs_str = ', '.join(f'{key}: {repr(value)}' for key, value in kwargs_items[:2]) or None
        if len(kwargs_items) > 2:
            kwargs_str += ', ...'

        logger.event(f"CLASS <{self.parent.__class__.__name__}> (tag={self.parent.tag}) CALLS EVENT <{self.event_name}> (<{self.function.__name__}>) (agrs={args_str}, kwargs={kwargs_str})")
        return self.function(*args, **kwargs)


@dataclass
class Buffer:
    """
    Represents a container for storing method and position used in text interface.

    :param function: Function that returns text or buffers list that will be printed in terminal
    :type function: typing.Callable[[], Union[str, List[Self]]]
    :param position: Position at which it will be printed in terminal
    :type position: Position
    :param size: Size of buffer in terminal
    :type size: Size
    """
    function: Callable[[], Union[str, List[Self]]] = None
    position: Position = None
    size: Size = None


@dataclass
class Collection(list):
    """
    Represents an extended list and provides type safety for elements that must implement BaseElementInterface interface

    :param interface_level: Specifies the elements type that the collection can hold
    :type interface_level: typing.Type
    """
    interface_level: Type = BaseElementInterface
    """Specifies the elements type that the collection can hold"""

    def __init__(self, elements: List[interface_level] = None):
        if elements is None:
            elements = []
        for element in elements:
            if not isinstance(element, self.interface_level):
                raise TypeError(f"Expected type '{self.interface_level}', got '{type(element)}' instead")
        super().__init__(elements)

    def __str__(self) -> str:
        return f"[{', '.join(str(element) for element in self)}]"

    def append(self, element: interface_level):
        if not isinstance(element, self.interface_level):
            raise TypeError(f"Expected type '{self.interface_level}', got '{type(element)}' instead")
        super().append(element)

    def insert(self, index: int, element: interface_level):
        if not isinstance(element, self.interface_level):
            raise TypeError(f"Expected type '{self.interface_level}', got '{type(element)}' instead")
        super().insert(index, element)

    def set_elements_attribute(self,
                               attribute: Text,
                               value: Any,
                               rule: Callable[[BaseElementInterface], bool] = lambda element: True) -> Self:
        """
        Sets attribute value for elements that satisfy rule condition.

        :param attribute: Attribute name to be set
        :type attribute: typing.Text
        :param value: Value to set for attribute
        :type value: typing.Any
        :param rule: Condition function for filtering elements
        :type rule: typing.Callable[[BaseElementInterface], bool]
        :return: Filtered collection of elements
        :rtype: Collection
        """
        return_list: Collection = Collection()
        for element in self:
            if rule(element):
                setattr(element, attribute, value)
                return_list.append(element)
        return return_list

    def get_elements_collection(self,
                                rule: Callable[[BaseElementInterface], bool] = lambda element: True) -> Self:
        """
        Returns filtered collection of elements that satisfy rule condition.

        :param rule: Condition function for filtering elements
        :type rule: typing.Callable[[BaseElementInterface], bool]
        :return: Filtered collection of elements
        :rtype: Collection
        """
        return_list: Collection = Collection()
        for element in self:
            if rule(element):
                return_list.append(element)
        return return_list

    def call_elements_event(self,
                            event: Text,
                            rule: Callable[[BaseElementInterface], bool] = lambda element: True,
                            args: List = None,
                            kwargs: Dict = None) -> List[Any]:
        """
        Calls event with args and kwargs arguments on elements that satisfy rule condition.

        :param event: Event name
        :type event: typing.Text
        :param rule: Condition function for filtering elements
        :type rule: typing.Callable[[BaseElementInterface], bool]
        :param args: Positional arguments that will be passed to event
        :type args: typing.List
        :param kwargs: Named arguments that will be passed to event
        :type kwargs: typing.Dict
        :return: Returned values of filtered collection elements
        :rtype: typing.List[Any]
        """
        args, kwargs = args or [], kwargs or {}
        return_list: List[Any] = []
        for element in self.get_elements_collection(rule):
            return_list.append(getattr(element.event.call, event)(*args, **kwargs))
        return return_list
