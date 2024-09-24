from . import BaseElement
from ..core import Terminal


class Root:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.console = Terminal()
        cls.layout: BaseElement
        return instance

    def update(self):
        self.layout.update()

    def read_keys(self):
        self.layout.event.call.key_pressed(self.console.read())

    def set_layout(self, layout: BaseElement) -> None:
        self.layout = layout

    def refresh(self) -> None:
        self.console.set_buffer(self.layout.build())
