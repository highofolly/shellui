from .interfaces import BaseElementInterface
from .debug import logging
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import *
from enum import Enum


class ElementState(Enum):
    MISSED      = 0
    SELECTED    = 1


@dataclass
class Dimensions(ABC):
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
    function: Callable
    _lambda: Callable


@dataclass
class EventUnit:
    """
    Represents event unit that associated function with EventManager class
    """
    parent: BaseElementInterface = BaseElementInterface
    """Parent class object"""

    def __setfunc__(self, function: Callable = None):
        """
        Sets the function for given event

        :param function: Function that will be called when the event is triggered
        """
        self.function: Callable = function

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

        logging.event(f"CLASS <{self.parent.__class__.__name__}> (tag={self.parent.tag}) CALLS EVENT <{self.function.__name__}> (agrs={args_str}, kwargs={kwargs_str})")
        return self.function(*args, **kwargs)


@dataclass
class Buffer:
    """
    Represents a container for storing method and position used in text interface
    """
    function: Callable = None
    """Method that will be called to get data"""
    position: Position = None
    """Position (x, y) on screen to display data"""
    size: Size = None


@dataclass
class Collection(list):
    """
    Represents an extended list and provides type safety for elements that must implement BaseElementInterface interface
    """
    interface_level: Type = BaseElementInterface

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
                               item: str,
                               value: Any,
                               rule: Callable = lambda element: True) -> Self:
        """
        Sets attribute value for elements that match condition

        :param item: Attribute name to be set
        :param value: Value to set for attribute
        :param rule: Condition function to filter elements
        :return: Filtered collection
        """
        return_list: Collection = Collection()
        for element in self:
            if rule(element):
                setattr(element, item, value)
                return_list.append(element)
        return return_list

    def get_elements_collection(self,
                                rule: Callable = lambda element: True) -> Self:
        """
        Returns a elements collection that match condition

        :param rule: Condition function to filter elements
        :return: Filtered collection
        """
        return_list: Collection = Collection()
        for element in self:
            if rule(element):
                return_list.append(element)
        return return_list

    def call_elements_event(self,
                            event: str,
                            rule: Callable = lambda element: True,
                            args: List = None,
                            kwargs: dict = None) -> List[Any]:
        """
        Raises an event on elements that match a condition with the given arguments

        :param event: Event name
        :param rule: Condition function to filter elements
        :param args: Positional arguments that will be passed to event
        :param kwargs: Named arguments that will be passed to event
        :return: Returned values of filtered collection elements
        """
        args, kwargs = args or [], kwargs or {}
        return_list: List[Any] = []
        for element in self.get_elements_collection(rule):
            return_list.append(getattr(element.event.call, event)(*args, **kwargs))
        return return_list
