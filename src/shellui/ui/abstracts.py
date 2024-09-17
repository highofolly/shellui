from .. import logging
from ..core.overloads import ABC, abstractmethod
from ..core.handler import EventManager
from ..core.typings import Buffer, List


class BaseElement(ABC):
    def __init__(self, *args, **kwargs):
        self.event = EventManager()
        self.event.create.build(self.build)
        self.event.create.update(self.update)
        self.event.create.key_pressed(self.key_pressed)
        logging.debug(f"<{__name__}>: create class {self.__class__} (agrs={args}, kwargs={kwargs})")

    @abstractmethod
    def build(self) -> Buffer:
        raise NotImplementedError

    def key_pressed(self, key_char: int) -> None: ...

    def update(self) -> None: ...


class AbstractWidget(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractWidget, self).__init__(*args, **kwargs)
        self.event.create.output(self.output)

    @abstractmethod
    def output(self) -> str:
        raise NotImplementedError

    def build(self) -> Buffer:
        return Buffer(self.event.call.output)


class AbstractLayout(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractLayout, self).__init__(*args, **kwargs)
        self.elements: List[BaseElement] = []
        self.cursor: int = 0
        self.event.create.adjust(self.adjust)

    def key_pressed(self, key_char: int) -> None:
        self.elements[self.cursor].event.call.key_pressed(key_char)

    @abstractmethod
    def adjust(self, buffer: Buffer) -> str:
        raise NotImplementedError

    def update(self) -> None:
        for i in self.get_elements():
            i.event.call.update()

    def build(self) -> Buffer:
        def create_buffer_list() -> str:
            ret: List[str] = []
            for i in self.get_elements():
                ret.append(self.event.call.adjust(i.event.call.build()))
            return "".join(ret)
        return Buffer(create_buffer_list)

    def get_elements(self) -> List[BaseElement]:
        return self.elements

    def add_element(self, element: BaseElement) -> BaseElement:
        self.elements.append(element)
        return element
