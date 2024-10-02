from dataclasses import dataclass, field
from typing import *
from .interfaces import *


@dataclass
class Buffer:
    """
    Represents a container for storing method and position used in text interface
    """
    method: Callable = None
    """Method that will be called to get data"""
    position: Tuple[int, int] = None
    """Position (x, y) on screen to display data"""
    kwargs: dict = None

    def __post_init__(self):
        if self.kwargs is not None:
            for name, key in self.kwargs.items():
                setattr(self, name, key)


@dataclass
class Collection(list):
    """
    Represents an extended list and provides type safety for elements that must implement BaseElementInterface interface
    """
    def append(self, element: BaseElementInterface):
        if not isinstance(element, BaseElementInterface):
            raise TypeError(f"Expected type 'BaseElement', got '{type(element)}' instead")
        super().append(element)

    def insert(self, index, element):
        if not isinstance(element, BaseElementInterface):
            raise TypeError(f"Expected type 'BaseElement', got '{type(element)}' instead")
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
        return_list: Collection = []
        for index, element in enumerate(self):
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
