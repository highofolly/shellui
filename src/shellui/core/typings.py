from dataclasses import dataclass, field
from typing import *
from .interfaces import *


@dataclass
class Position:
    x: int
    y: int

    def __iter__(self):
        for i in range(2):
            yield self.x if i == 0 else self.y


@dataclass
class Buffer:
    """
    Represents a container for storing method and position used in text interface
    """
    function: Callable = None
    """Method that will be called to get data"""
    position: Position = None
    """Position (x, y) on screen to display data"""
    size: Position = None


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
                               _lambda: Callable = lambda element: True) -> Self:
        """
        Sets attribute value for elements that match condition

        :param item: Attribute name to be set
        :param value: Value to set for attribute
        :param _lambda: Condition function to filter elements
        :return: Filtered collection
        """
        return_list: Collection = Collection()
        for element in self:
            if _lambda(element):
                setattr(element, item, value)
                return_list.append(element)
        return return_list

    def get_elements_collection(self,
                                _lambda: Callable = lambda element: True) -> Self:
        """
        Returns a elements collection that match condition

        :param _lambda: Condition function to filter elements
        :return: Filtered collection
        """
        return_list: Collection = Collection()
        for element in self:
            if _lambda(element):
                return_list.append(element)
        return return_list

    def call_elements_event(self,
                            event: str,
                            _lambda: Callable = lambda element: True,
                            args: List = None,
                            kwargs: dict = None) -> List[Any]:
        """
        Raises an event on elements that match a condition with the given arguments

        :param event: Event name
        :param _lambda: Condition function to filter elements
        :param args: Positional arguments that will be passed to event
        :param kwargs: Named arguments that will be passed to event
        :return: Returned values of filtered collection elements
        """
        args, kwargs = args or [], kwargs or {}
        return_list: List[Any] = []
        for element in self.get_elements_collection(_lambda):
            return_list.append(getattr(element.event.call, event)(*args, **kwargs))
        return return_list
