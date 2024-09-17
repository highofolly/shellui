from ..ui import AbstractWidget, AbstractLayout


class Label(AbstractWidget):
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.text = kwargs.pop("text")

    def output(self):
        return self.text


class Button(Label):
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.event.create.on_click(self.on_click)
        self.event.create.key_pressed(
            lambda key_char: self.event.call.on_click() if key_char == 10 else None)

    def on_click(self) -> None: ...


class HLayout(AbstractLayout):
    def __init__(self):
        super(HLayout, self).__init__()

    def adjust(self, buffer):
        return f"{buffer.method()}\n"
