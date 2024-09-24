from .. import logging
from ..core import BaseElementInterface, EventManager, Buffer, Collection, Tuple, List, Any, abstractmethod


class BaseElement(BaseElementInterface):
    def __init__(self, *args, **kwargs):
        self.event = EventManager()
        self.event.create.build(self.build)
        self.event.create.update(self.update)
        self.event.create.key_pressed(lambda: None)
        self.position = kwargs.pop("position", [0, 0])
        logging.debug(f"CREATE CLASS <{self.__class__.__name__}> (agrs={args}, kwargs={kwargs})")

    @abstractmethod
    def build(self) -> Buffer:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> Any:
        raise NotImplementedError


class AbstractWidget(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractWidget, self).__init__(*args, **kwargs)
        self.event.create.output(self.output)

    @abstractmethod
    def output(self) -> str:
        raise NotImplementedError

    def build(self) -> Buffer:
        return Buffer(self.event.call.output, self.position)


class AbstractLayout(BaseElement):
    def __init__(self, *args, **kwargs):
        super(AbstractLayout, self).__init__(*args, **kwargs)
        self.elements: Collection = Collection()
        self.event.create.adjust(self.adjust)
        self.event.create.key_pressed(self.key_pressed)

    @abstractmethod
    def adjust(self, buffer: Buffer) -> str:
        raise NotImplementedError

    def key_pressed(self, key_char: int) -> Any: ...

    def update(self) -> Any:
        return self.elements.run_method("update")

    def add_element(self, element: BaseElement, position: Tuple[int, int] = None) -> BaseElement:
        element.position = position or [0, 0]
        self.elements.append(element)
        return element

    def build(self) -> Buffer:
        def create_buffer_list() -> List[Buffer]:
            ret: List[Buffer] = []
            for element in self.elements:
                element_buffer = element.event.call.build()
                ret.append(Buffer(method=lambda: self.event.call.adjust(element_buffer),
                                  position=element_buffer.position))
            return ret

        return Buffer(create_buffer_list, self.position)
