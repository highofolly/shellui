from .. import logging
from ..core import BaseElementInterface, EventManager, Buffer, Collection, Tuple, List, Any, Union, abstractmethod


class BaseElement(BaseElementInterface):
    """
    Represents abstract base class for all interface elements and layouts
    """

    def __init__(self, *args, **kwargs):
        """
        :param position: Element position in [x, y] format
        """
        self.event = EventManager(self)
        self.position = kwargs.pop("position", [0, 0])

        self.event.create.update(self.update)
        self.event.create.key_pressed(self.key_pressed)
        self.event.create.render(self.render)
        self.event.create.build(self.build)
        logging.debug(f"CREATE CLASS <{self.__class__.__name__}> (agrs={args}, kwargs={kwargs})")

    @abstractmethod
    def update(self) -> Any:
        """
        Updates element state
        """
        raise NotImplementedError

    @abstractmethod
    def key_pressed(self, key_char) -> Any:
        """
        Handles key press
        """
        raise NotImplementedError

    @abstractmethod
    def render(self) -> Union[str, Collection]:
        """
        Builds element contents

        :return: String if the widget is last one, else elements list
        """
        raise NotImplementedError

    def build(self) -> Buffer:
        """
        Builds element buffer

        :return: Element buffer
        """
        return Buffer(self.event.call.render, self.position)


class AbstractWidget(BaseElement):
    """
    Represents abstract class for interface widgets
    """

    def __init__(self, *args, **kwargs):
        super(AbstractWidget, self).__init__(*args, **kwargs)


class AbstractLayout(BaseElement):
    """
    Represents abstract class for interface elements layout
    """

    def __init__(self, *args, **kwargs):
        super(AbstractLayout, self).__init__(*args, **kwargs)
        self.elements: Collection = Collection()

    def add_element(self, element: BaseElement, position: Tuple[int, int] = None) -> BaseElement:
        """
        Adds element to collection

        :param element: Element for adding to collection
        :param position: Element position to set position
        :return: Same element
        """
        element.position = position or element.position
        self.elements.append(element)
        return element
