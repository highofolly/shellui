from .. import logging
from ..core import BaseElementInterface, EventManager, Buffer, Collection, Tuple, List, Any, Union, abstractmethod


class BaseElement(BaseElementInterface):
    def __init__(self, *args, **kwargs):
        self.event = EventManager(self)
        self.position = kwargs.pop("position", [0, 0])

        self.event.create.update(self.update)
        self.event.create.key_pressed(self.key_pressed)
        self.event.create.render(self.render)
        self.event.create.build(self.build)
        logging.debug(f"CREATE CLASS <{self.__class__.__name__}> (agrs={args}, kwargs={kwargs})")

    @abstractmethod
    def update(self) -> Any: raise NotImplementedError
    @abstractmethod
    def key_pressed(self, key_char) -> Any: raise NotImplementedError
    @abstractmethod
    def render(self) -> Union[str, Collection]: raise NotImplementedError

    def build(self) -> Buffer:
        return Buffer(self.event.call.render, self.position)


class AbstractWidget(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractWidget, self).__init__(*args, **kwargs)


class AbstractLayout(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractLayout, self).__init__(*args, **kwargs)
        self.elements: Collection = Collection()

    def add_element(self, element: BaseElement, position: Tuple[int, int] = None) -> BaseElement:
        element.position = position or element.position
        self.elements.append(element)
        return element