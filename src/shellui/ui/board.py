from .abstracts import AbstractWidget, AbstractLayout, ElementState, BaseElement
from ..common import Collection
from ..common.debug import logger
from ..common.types import List, Any, Size, Buffer
from ..core.handler import CursorController
import curses


class BaseFlags(BaseElement.BaseFlags):
    isActiveElement: bool


class Widget(AbstractWidget):
    """
    Represents abstract class of widget for layout
    """
    class_base_tag = "Widget"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags: Widget.BaseFlags = self.flags
        self.flags.isActiveElement = False
        self.keyboard.add_keyboard_event(self.on_click, lambda key_char: key_char == 10)

    def update(self): ...
    def render(self): ...
    def on_click(self, key: int) -> Any: ...
    def get_size(self) -> Size: ...


class Layout(AbstractLayout):
    class_base_tag = "Layout"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags: Widget.BaseFlags = self.flags
        self.cursor: CursorController = CursorController(self.elements)
        self.flags.isActiveElement = True
        self.UP_KEYS = [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_BTAB]
        self.DOWN_KEYS = [curses.KEY_DOWN, curses.KEY_RIGHT, 9]
        self.keyboard.add_keyboard_event(self.on_click, lambda key_char: key_char == 10)
        self.keyboard.add_keyboard_event(self.key_up, lambda key_char: key_char in self.UP_KEYS)
        self.keyboard.add_keyboard_event(self.key_down, lambda key_char: key_char in self.DOWN_KEYS)

    def on_click(self, key) -> Any:
        current = self.cursor.current
        if current:
            return current.keyboard.key_pressed(key)

    def key_up(self, key) -> bool:
        if not any(self.cursor.current.keyboard.key_pressed(key)):
            if self.cursor.move(-1, lambda current: current.flags.isActiveElement):
                return True
            return False
        else:
            return True

    def key_down(self, key) -> bool:
        lox = self.cursor.current.keyboard.key_pressed(key)
        if not any(lox):
            if self.cursor.move(1, lambda current: current.flags.isActiveElement):
                return True
            return False
        else:
            return True

    def select(self):
        self.cursor.current.event.call.select()
        return super().select()

    def deselect(self):
        self.elements.call_elements_event("deselect", lambda element: element.flags.isActiveElement)
        return super().deselect()

    def get_size(self):
        self.size = Size(0, 0)
        element: BaseElement
        for element in self.elements:
            self.size.height += element.size.height
            if element.size.width > self.size.width:
                self.size.width = element.size.width
        return self.size

    def update(self):
        return_list = super().update()

        self.elements.call_elements_event("get_size", lambda element: not element.flags.isFixedSize)
        if not self.flags.isFixedSize:
            self.event.call.get_size()

        self.event.call.deselect()
        self.event.call.select()
        return return_list

    def __style__(self, element):
        if element.state == ElementState.SELECTED and element.flags.isActiveElement:
            return self.cursor.style % {"widget": element.render()}
        else:
            return element.render()


class Label(Widget):
    """
    Represents graphic text label element
    """
    class_base_tag = "Label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text: str = kwargs.pop("text", "")

    def get_size(self):
        lines = self.text.split('\n')
        self.size = Size(max(len(line) for line in lines), len(lines))
        return self.size

    def render(self):
        return self.text

    def set_text(self, text: str):
        self.text = text


class Button(Label):
    """
    Represents graphical button element
    """
    class_base_tag = "Button"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags.isActiveElement = True


class CheckBox(Label):
    """
    Represents graphical checkbox element
    """
    class_base_tag = "CheckBox"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags.isActiveElement = True
        self.flags.isChecked = False

    def get_size(self):
        lines = self.text.split('\n')
        self.size = Size(4 + max(len(line) for line in lines), len(lines))
        return self.size

    def on_click(self, key):
        self.flags.isChecked = False if self.isChecked() else True

    def isChecked(self):
        return self.flags.isChecked

    def render(self):
        return f"[*] {self.text}" if self.isChecked() else f"[ ] {self.text}"


class VLayout(Layout):
    """
    Represents a vertical layout
    """
    class_base_tag = "VLayout"

    def __align__(self, elements):
        matrix: List[Buffer] = []
        temp_pos = 0
        for buffer in sorted(elements.call_elements_event("build"), key=lambda element: element.position.y):
            buffer.position.y = temp_pos
            temp_pos += buffer.size.height
            matrix.append(buffer)
        return matrix


class HLayout(Layout):
    """
    Represents a vertical layout
    """
    class_base_tag = "HLayout"

    def __align__(self, elements):
        matrix: List[Buffer] = []
        temp_pos = 0
        for buffer in sorted(elements.call_elements_event("build"), key=lambda element: element.position.x):
            buffer.position.x = temp_pos
            temp_pos += buffer.size.width + len(self.cursor.style % {"widget": ""})
            matrix.append(buffer)
        return matrix
