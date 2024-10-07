from .. import logging
from ..core import BaseElementInterface, EventManager, FlagsManager, KeyboardManager, Buffer, Position, Collection, Tuple, Any, Union, abstractmethod
from enum import Enum


class ElementState(Enum):
    MISSED      = 0
    SELECTED    = 1


class BaseElement(BaseElementInterface):
    """
    Represents abstract base class for all interface elements and layouts
    """
    class_base_tag = "BaseElement"

    def __init__(self, *args, **kwargs):
        """
        :param position: Element position in [x, y] format
        """
        self.position: Position = Position(*kwargs.pop("position", [0, 0]))
        self.size: Position = Position(0, 0)
        self.tag = kwargs.pop("tag", self.class_base_tag)
        self.state: ElementState = ElementState.MISSED

        self.flags: FlagsManager = FlagsManager()
        self.keyboard: KeyboardManager = KeyboardManager(self)
        self.event: EventManager = EventManager(self)
        self.event.create.update(self.update)
        self.event.create.render(self.render)
        self.event.create.build(self.build)
        self.event.create.select(self.select)
        self.event.create.deselect(self.deselect)
        self.flags.is_fixed_size = False
        logging.create(f"CREATE CLASS <{self.__class__.__name__}> (agrs={args}, kwargs={kwargs})")

    def select(self) -> None:
        """
        Sets widget state to "ElementState.SELECTED"
        """
        self.state = ElementState.SELECTED

    def deselect(self) -> None:
        """
        Sets widget state to "ElementState.MISSED"
        """
        self.state = ElementState.MISSED

    def set_fixed_size(self, size: Union[Position, Tuple[int, int]]):
        self.flags.is_fixed_size = True
        self.size = size if isinstance(size, Position) else Position(*size)

    def set_floating_size(self):
        self.flags.is_fixed_size = False

    @abstractmethod
    def update(self) -> Any:
        """
        Updates element state
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
        return Buffer(self.event.call.render, self.position, self.size)


class AbstractWidget(BaseElement):
    """
    Represents abstract class for interface widgets
    """
    class_base_tag = "AbstractWidget"

    def __init__(self, *args, **kwargs):
        super(AbstractWidget, self).__init__(*args, **kwargs)


class AbstractLayout(BaseElement):
    """
    Represents abstract class for interface elements layout
    """
    class_base_tag = "AbstractWidget"

    def __init__(self, *args, **kwargs):
        super(AbstractLayout, self).__init__(*args, **kwargs)
        self.elements: Collection = Collection()

    def add_element(self, element: BaseElement, position: Union[Position, Tuple[int, int]] = None) -> BaseElement:
        """
        Adds element to collection

        :param element: Element for adding to collection
        :param position: Element position to set position
        :return: Same element
        """
        element.position = (position if isinstance(position, Position) else Position(*position)) if position else element.position
        self.elements.append(element)
        return element
