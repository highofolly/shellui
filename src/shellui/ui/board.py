from . import AbstractWidget, AbstractLayout
from .. import logging
from ..core import curses, List, Any, Union, Buffer
from enum import Enum


class ElementState(Enum):
    INACTIVE = 0
    ACTIVE = 1
    SELECTED = 2


class ActiveWidget(AbstractWidget):
    def __init__(self, *args, **kwargs):
        super(ActiveWidget, self).__init__(*args, **kwargs)
        self.state: ElementState = ElementState.INACTIVE
        self.event.create.on_click(self.on_click)
        self.event.create.on_key_press(self.on_key_press)

    def update(self) -> Any: ...
    def on_click(self) -> Any: ...
    def on_key_press(self, key_char) -> Any: ...

    def key_pressed(self, key_char) -> Any:
        if key_char == 10:
            return self.event.call.on_click()
        else:
            return self.event.call.on_key_press(key_char)

    def select(self):
        self.state = ElementState.SELECTED

    def deselect(self):
        self.state = ElementState.INACTIVE


class StaticWidget(AbstractWidget):
    def __init__(self, *args, **kwargs):
        super(AbstractWidget, self).__init__(*args, **kwargs)
        self.state: ElementState = ElementState.INACTIVE

    def update(self) -> Any: ...

    def key_pressed(self, key_char) -> Any: ...


class Label(StaticWidget):
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.text = kwargs.pop("text")

    def output(self):
        return self.text


class Button(ActiveWidget):
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.text = kwargs.pop("text")

    def output(self):
        return self.text if self.state == ElementState.INACTIVE else f"> {self.text}"


class HLayout(AbstractLayout):
    def __init__(self, *args, **kwargs):
        super(HLayout, self).__init__(*args, **kwargs)
        self.cursor: int = 0
        self.UP_KEYS = [curses.KEY_UP, curses.KEY_LEFT]
        self.DOWN_KEYS = [curses.KEY_DOWN, curses.KEY_RIGHT]

    def update(self) -> Any:
        self.elements.get_elements_collection(lambda element: isinstance(element, ActiveWidget))[self.cursor].select()
        return self.elements.run_elements_method("update")

    def key_pressed(self, key_char: int) -> Any:
        self.elements.set_elements_attribute("state", ElementState.INACTIVE)
        if key_char in self.UP_KEYS:
            self.cursor = self.cursor - 1 if self.cursor > 0 else len(self.elements) - 1
        elif key_char in self.DOWN_KEYS:
            self.cursor = self.cursor + 1 if self.cursor < len(self.elements) - 1 else 0
        else:
            return self.elements[self.cursor].event.call.key_pressed(key_char)

    def output(self) -> Union[str, List[Buffer]]:
        ret: List[Buffer] = []
        for element in self.elements:
            ret.append(element.event.call.build())
        return ret
