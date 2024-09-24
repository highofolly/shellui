from dataclasses import dataclass, field
from typing import *
from .interfaces import *


@dataclass
class Buffer:
    method: Callable
    kwargs: dict = None

    def __post_init__(self):
        if self.kwargs is not None:
            for name, key in self.kwargs.items():
                setattr(self, name, key)


@dataclass
class Collection(list):
    def append(self, element):
        if not isinstance(element, BaseElementInterface):
            raise TypeError(f"Expected type 'BaseElement', got '{type(element)}' instead")
        super().append(element)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def insert(self, index, element):
        if not isinstance(element, BaseElementInterface):
            raise TypeError(f"Expected type 'BaseElement', got '{type(element)}' instead")
        super().insert(index, element)

    def set_attribute(self,
                      item: str,
                      value: Any,
                      _lambda: Callable = lambda element: True) -> Self:
        return_list: Collection = Collection()
        for element in self:
            if _lambda(element):
                setattr(element, item, value)
                return_list.append(element)
        return return_list

    def get_collection(self,
                      _lambda: Callable = lambda element: True) -> Self:
        return_list: Collection = []
        for index, element in enumerate(self):
            if _lambda(element):
                return_list.append(element)
        return return_list

    def run_method(self,
                   method: str,
                   _lambda: Callable = lambda element: True,
                   args: List = None,
                   kwargs: dict = None) -> List[Any]:
        args, kwargs = args or [], kwargs or {}
        return_list: List[Any] = []
        for element in self.get_collection(_lambda):
            return_list.append(getattr(element, method)(*args, **kwargs))
        return return_list
