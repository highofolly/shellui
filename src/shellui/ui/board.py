from .abstracts import AbstractWidget, AbstractLayout, ElementState, BaseElement
from ..common.debug import logging
from ..common.types import List, Any, Size, Buffer
import curses


class BaseFlags(BaseElement.BaseFlags):
    is_active_element: bool


class Widget(AbstractWidget):
    """
    Represents abstract class of widget for layout
    """
    class_base_tag = "Widget"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags: Widget.BaseFlags = self.flags
        self.text: str = ""
        self.flags.is_active_element = False
        self.set_text(kwargs.pop("text", ""))
        self.keyboard.add_keyboard_event(self.on_click, lambda key_char: key_char == 10)

    def update(self): ...
    def render(self): ...
    def on_click(self) -> Any: ...
    def get_size(self) -> Size: ...

    def set_text(self, text: str):
        self.text = text


class Layout(AbstractLayout):
    class_base_tag = "Layout"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags: Widget.BaseFlags = self.flags
        self.cursor: int = 0
        self.cursor_skin: str = kwargs.pop("cursor_skin", "> ")
        self.flags.is_active_element = True
        self.UP_KEYS = [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_BTAB]
        self.DOWN_KEYS = [curses.KEY_DOWN, curses.KEY_RIGHT, 9]
        self.keyboard.add_keyboard_event(self.on_click, lambda key_char: key_char == 10)
        self.keyboard.add_keyboard_event(self.key_up, lambda key_char: key_char in self.UP_KEYS)
        self.keyboard.add_keyboard_event(self.key_down, lambda key_char: key_char in self.DOWN_KEYS)

    def set_cursor_skin(self, skin: str) -> None:
        self.cursor_skin = skin

    def on_click(self) -> Any:
        return self.elements.get_elements_collection(lambda element: element.flags.is_active_element)[self.cursor].keyboard.key_pressed(10)

    def key_up(self) -> bool:
        if self.elements.get_elements_collection(lambda element: element.flags.is_active_element)[self.cursor].keyboard.key_pressed(curses.KEY_UP) != [1]:
            if self.cursor > 0:
                self.cursor -= 1
                return True

    def key_down(self) -> bool:
        if self.elements.get_elements_collection(lambda element: element.flags.is_active_element)[self.cursor].keyboard.key_pressed(curses.KEY_DOWN) != [1]:
            if self.cursor < len(self.elements.get_elements_collection(lambda element: element.flags.is_active_element)) - 1:
                self.cursor += 1
                return True

    def select(self):
        self.elements.get_elements_collection(lambda element: element.flags.is_active_element)[self.cursor].event.call.select()
        return super().select()

    def deselect(self):
        self.elements.call_elements_event("deselect", lambda element: element.flags.is_active_element)
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

        self.elements.call_elements_event("get_size", lambda element: not element.flags.is_fixed_size)
        if not self.flags.is_fixed_size:
            self.event.call.get_size()

        self.event.call.deselect()
        self.event.call.select()
        return return_list

    def style(self, element: Widget) -> str:
        if element.state == ElementState.SELECTED and element.flags.is_active_element:
            return f"{self.cursor_skin}{element.render()}"
        else:
            return element.render()

    def render(self): ...


class Label(Widget):
    """
    Represents graphic text label element
    """
    class_base_tag = "Label"

    def get_size(self):
        lines = self.text.split('\n')
        self.size = Size(max(len(line) for line in lines), len(lines))
        return self.size

    def render(self):
        return self.text


class Button(Widget):
    """
    Represents graphical button element
    """
    class_base_tag = "Button"

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.flags.is_active_element = True

    def get_size(self):
        lines = self.text.split('\n')
        self.size = Size(max(len(line) for line in lines), len(lines))
        return self.size

    def render(self):
        return self.text


class CheckBox(Widget):
    """
    Represents graphical checkbox element
    """
    class_base_tag = "CheckBox"

    def __init__(self, *args, **kwargs):
        super(CheckBox, self).__init__(*args, **kwargs)
        self.flags.is_active_element = True
        self.flags.is_checked = False

    def get_size(self):
        lines = self.text.split('\n')
        self.size = Size(4 + max(len(line) for line in lines), len(lines))
        return self.size

    def on_click(self):
        self.flags.is_checked = False if self.is_checked() else True

    def is_checked(self):
        return self.flags.is_checked

    def render(self):
        return f"[*] {self.text}" if self.is_checked() else f"[ ] {self.text}"


class VLayout(Layout):
    """
    Represents a vertical layout
    """
    class_base_tag = "VLayout"

    def render(self):
        matrix: List[Buffer] = []
        temp_pos = 0
        temp_elements = self.elements.get_elements_collection()
        for element in temp_elements.get_elements_collection(lambda element: isinstance(element, Widget)):
            element.event.create.render((lambda element: lambda: self.style(element))(element))
        for buffer in sorted(temp_elements.call_elements_event("build"), key=lambda element: element.position.y):
            buffer.position.y = temp_pos
            temp_pos += buffer.size.height
            matrix.append(buffer)
        return matrix


class HLayout(Layout):
    """
    Represents a vertical layout
    """
    class_base_tag = "HLayout"

    def render(self):
        matrix: List[Buffer] = []
        temp_pos = 0
        temp_elements = self.elements.get_elements_collection()
        for element in temp_elements.get_elements_collection(lambda element: isinstance(element, Widget)):
            element.event.create.render((lambda element: lambda: self.style(element))(element))
        for buffer in sorted(temp_elements.call_elements_event("build"), key=lambda element: element.position.x):
            buffer.position.x = temp_pos
            temp_pos += buffer.size.width + len(self.cursor_skin)
            matrix.append(buffer)
        return matrix
