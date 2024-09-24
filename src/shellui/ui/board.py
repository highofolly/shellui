from . import AbstractWidget, AbstractLayout
from .. import logging
from ..core import curses, List, Any, Buffer


class Label(AbstractWidget):
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.text = kwargs.pop("text")
        self.state = False
        self.event.create.is_active(self.is_active)

    def is_active(self):
        return False

    def output(self):
        return self.text


class Button(Label):
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.event.create.on_click(self.on_click)
        self.state = True
        self.event.create.key_pressed(
            lambda key_char: self.event.call.on_click() if key_char == curses.KEY_ENTER else None)

    def is_active(self):
        return True

    def on_click(self) -> None: ...


class HLayout(AbstractLayout):
    def __init__(self):
        super(HLayout, self).__init__()
        self.UP_KEYS = [curses.KEY_UP, curses.KEY_LEFT]
        self.DOWN_KEYS = [curses.KEY_DOWN, curses.KEY_RIGHT]

    def key_pressed(self, key_char: int) -> None:
        self.elements.set_attribute("state", False)
        if key_char in self.UP_KEYS:
            self.cursor -= 1
        elif key_char in self.DOWN_KEYS:
            self.cursor += 1
        else:
            super().key_pressed(key_char)
            return
        self.elements.get_collection(lambda element: element.is_active())[self.cursor].state = True

    def adjust(self, buffer):
        return f"{buffer.method()}\n"
