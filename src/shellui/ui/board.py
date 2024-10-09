from . import AbstractWidget, AbstractLayout, ElementState
from .. import logging
from ..core import curses, List, Any, Position, Buffer


class Widget(AbstractWidget):
    """
    Represents abstract class of widget for layout
    """
    class_base_tag = "Widget"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text: str = ""
        self.set_text(kwargs.pop("text", ""))
        self.keyboard.add_keyboard_event(self.on_click, lambda key_char: key_char == 10)

    def update(self): ...
    def render(self): ...
    def on_click(self) -> Any: ...

    def set_text(self, text: str):
        self.text = text
        if not self.flags.is_fixed_size:
            lines = self.text.split('\n')
            self.size = Position(max(len(line) for line in lines), len(lines))


class Layout(AbstractLayout):
    class_base_tag = "Layout"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor: int = 0
        self.cursor_skin: str = kwargs.pop("cursor_skin", "> ")
        self.flags.is_active_element = True
        self.UP_KEYS = [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_BTAB]
        self.DOWN_KEYS = [curses.KEY_DOWN, curses.KEY_RIGHT, 9]
        self.keyboard.add_keyboard_event(self.on_click, lambda key_char: key_char == 10)
        self.keyboard.add_keyboard_event(self.key_up, lambda key_char: key_char in self.UP_KEYS)
        self.keyboard.add_keyboard_event(self.key_down, lambda key_char: key_char in self.DOWN_KEYS)

    def set_cursor_skin(self, skin: str):
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

    def update(self):
        return_list = super().update()
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

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.flags.is_active_element = False

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

    def render(self):
        return self.text


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
            temp_pos += buffer.size.y
            matrix.append(buffer)
        return matrix
