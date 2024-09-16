from ..core.overloads import ABC, abstractmethod
from ..core.handler import EventManager
from ..core.typings import Buffer, List


class BaseElement(ABC):
    def __init__(self, *args, **kwargs):
        self.event = EventManager()
        self.event.create.build(self.build)
        self.event.create.update(self.update)

    @abstractmethod
    def build(self) -> Buffer:
        raise NotImplementedError

    def update(self) -> None: ...


class AbstractWidget(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractWidget, self).__init__(*args, **kwargs)
        self.event.create.output(self.output)
        self.event.create.on_hover(self.on_hover)
        self.event.create.on_pressed(self.on_pressed)

    @abstractmethod
    def output(self) -> str:
        raise NotImplementedError

    def on_hover(self) -> None: ...
    def on_pressed(self) -> None: ...

    def build(self) -> Buffer:
        return Buffer(self.event.call.output)


class AbstractLayout(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractLayout, self).__init__(*args, **kwargs)
        self.elements: List[BaseElement] = []
        self.event.create.adjust(self.adjust)

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
