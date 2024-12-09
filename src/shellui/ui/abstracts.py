from ..common.types import Buffer, Position, Size, Collection, ElementState, Tuple, Any, Union, List, overload, runtime_checkable, Protocol, ABC, abstractmethod, Self
from ..common.debug import logger
from ..core.handler import EventManager, FlagsController, KeyboardHandler


class BaseElement(ABC):
    """
    Represents abstract base class for all interface elements and layouts
    """
    class_base_tag = "BaseElement"

    @runtime_checkable
    class BaseFlags(Protocol):
        isFixedSize: bool
        def set_flag(self, key, value) -> None: ...
        def get_flag(self, key) -> bool: ...
        def __getattr__(self, key) -> bool: ...
        def __setattr__(self, key: str, value: bool) -> None: ...

    def __init__(self, *args, **kwargs):
        """
        :param position: Element position in [x, y] format
        """
        self.position: Position = Position(*kwargs.pop("position", [0, 0]))
        self.size: Size = Size(0, 0)
        self.tag: str = kwargs.pop("tag", self.class_base_tag)
        self.state: ElementState = ElementState.MISSED

        self.flags: BaseElement.BaseFlags = FlagsController(self)
        self.keyboard: KeyboardHandler = KeyboardHandler(self)
        self.event: EventManager = EventManager(self)
        self.event.set_events(get_size=self.get_size,
                              update=self.update,
                              render=self.render,
                              build=self.build,
                              select=self.select,
                              deselect=self.deselect)
        self.flags.isFixedSize = False

        if "flags" in kwargs:
            for key, value in kwargs["flags"].items():
                self.flags.set_flag("key", value)
        logger.create(f"CREATE CLASS <{self.__class__.__name__}> (tag={self.tag}) (agrs={args}, kwargs={kwargs})")

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

    @overload
    def set_fixed_size(self, size: Union[Size, Tuple[int, int], List[int]]) -> None: ...
    @overload
    def set_fixed_size(self, width: int, height: int) -> None: ...

    def set_fixed_size(self, *args, **kwargs):
        self.flags.isFixedSize = True
        width, height = kwargs.pop("width", None), kwargs.pop("height", None)
        size = kwargs.pop("size", None)
        if len(args) == 1:
            self.size = Size(*args[0])
        elif len(args) == 2:
            self.size = Size(*args)
        elif width and height:
            self.size = Size(width, height)
        elif size:
            self.size = Size(*size)

    def set_floating_size(self):
        self.flags.isFixedSize = False

    @abstractmethod
    def get_size(self) -> Size:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> Any:
        """
        Updates element state
        """
        raise NotImplementedError

    @abstractmethod
    def render(self) -> Union[str, List[Buffer]]:
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
    class_base_tag = "AbstractLayout"

    def __init__(self, *args, **kwargs):
        super(AbstractLayout, self).__init__(*args, **kwargs)
        self.elements: Collection = Collection()
        self.event.set.get_by_tag(self.search_elements_by_tag)

    @abstractmethod
    def __style__(self, element: Self) -> str:
        raise NotImplementedError
    @abstractmethod
    def __align__(self, elements: Collection) -> List[Buffer]:
        raise NotImplementedError

    @overload
    def add_elements(self, element: BaseElement, position: Union[Position, Tuple[int, int]] = None) -> BaseElement:
        """
        Adds element to collection and changes its position

        :param element: Element for adding to collection
        :param position: Element position to set position
        :return: Same element
        """

    @overload
    def add_elements(self, *elements: BaseElement) -> Collection:
        """
        Adds elements to collection

        :param elements: Elements for adding to collection
        :return: Collection same elements
        """

    def add_elements(self, *args, **kwargs):
        return_element = None
        if len(args) == 1 or kwargs.get("element", None):
            position = kwargs.get("position", None)
            return_element = args[0]
            if not return_element.flags.isFixedSize:
                if position:
                    return_element.position = (position if isinstance(position, Position) else Position(*position)) if position else return_element.position
            self.elements.append(return_element)
        elif len(args) > 1:
            self.elements.extend(args)
            return_element = Collection()
            return_element.extend(args)
        return return_element

    def search_elements_by_tag(self, tag: str) -> Collection:
        return (self.elements.get_elements_collection(lambda element: element.tag == tag) +
                sum(self.elements.call_elements_event("get_by_tag", lambda element: isinstance(element, AbstractLayout), args=[tag]), []))

    def update(self):
        return self.elements.call_elements_event("update")

    def render(self):
        temp_elements = self.elements.get_elements_collection()
        for element in temp_elements.get_elements_collection(lambda element: isinstance(element, AbstractWidget)):
            element.event.set.render((lambda element: lambda: self.__style__(element))(element))
        return self.__align__(temp_elements)
