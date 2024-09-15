from ..core.terminal import Terminal
from ..core.typings import List, Buffer
from .abstracts import AbstractLayout, BaseElement


class Root(AbstractLayout):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.console = Terminal()
        cls._layout: List[BaseElement]
        return instance

    def adjust(self, buffer: Buffer) -> str:
        return buffer.method()

    def set_layout(self, layout: AbstractLayout) -> None:
        self.elements = layout.elements[:]

    def refresh(self) -> None:
        self.console.set_buffer(self.build())
