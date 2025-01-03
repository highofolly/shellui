from .abstracts import BaseElement
from .board import Layout
from ..common import Collection
from ..core.terminal import Terminal


class Root(Layout):
    """
    Represents link between layout and terminal
    """
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.terminal = Terminal()
        cls.layout: BaseElement
        return instance

    def __style__(self, element): ...
    def __align__(self, elements): ...

    def update(self):
        """
        Updates layout's element state
        """
        self.layout.event.call.update()

    def read_keys(self):
        """
        Reads key in terminal and sends it to layout's key_pressed event
        """
        self.layout.keyboard.key_pressed(self.terminal.read())

    def set_layout(self, layout: BaseElement) -> None:
        """
        Sets main layout for root
        """
        self.layout = layout

    def render(self):
        self.refresh()

    def refresh(self) -> None:
        """
        Sets rendering buffer for terminal and builds layout's element buffer
        """
        self.terminal.set_buffer(self.layout.event.call.build())
