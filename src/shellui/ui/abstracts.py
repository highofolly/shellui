from ..core.overloads import ABC, abstractmethod
from ..core.handler import EventManager
from ..core.typings import Buffer, List


class BaseElement(ABC):
    def __init__(self, *args, **kwargs):
        self.event = EventManager()

    @abstractmethod
    def build(self) -> Buffer:
        raise NotImplementedError

    def update(self) -> None: ...


class AbstractWidget(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractWidget, self).__init__(*args, **kwargs)
        self.event.create.on_click(self.on_click)
        self.event.create.on_hover(self.on_hover)

    @abstractmethod
    def output(self) -> str:
        raise NotImplementedError

    def on_click(self) -> None: ...
    def on_hover(self) -> None: ...

    def build(self) -> Buffer:
        return Buffer(self.output)


class AbstractLayout(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractLayout, self).__init__(*args, **kwargs)
        self.elements: List[BaseElement] = []

    @abstractmethod
    def adjust(self, buffer: Buffer) -> str:
        raise NotImplementedError

    def build(self) -> Buffer:
        def create_buffer_list():
            ret: List[str] = []
            for i in self.elements:
                ret.append(self.adjust(i.build()))
            return "".join(ret)
        return Buffer(create_buffer_list)

    def add_widget(self, element: BaseElement) -> BaseElement:
        self.elements.append(element)
        return element
