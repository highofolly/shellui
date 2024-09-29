
v0.2-alpha.2 / 2024-09-29
==================

### added:
  * ui.board.HLayout.update method
  * ui.board.ElementState, ui.board.ActiveWidget and ui.board.StaticWidget classes
### changed:
  * ui.abstracts.BaseElement.build method
  * ui.abstracts.AbstractLayout.add_element method
  * hierarchy of ui.board.Label and ui.board.Button classes
  * ui.board.HLayout.key_pressed method
  * rename set_attribute, get_collection and run_method methods in core.typings.Collection class
  * move ui.abstracts.AbstractWidget.output method to ui.abstracts.BaseElement class
### deleted:
  * ui.board.HLayout.adjust method
  * ui.board.Button.is_active, Button.update, Button.on_click methods
  * ui.board.Label.is_active method
  * adjust, key_pressed, update and build methods in ui.abstracts.AbstractLayout class

v0.2-alpha.1 / 2024-09-24
==================

### added:
  * position argument in core.typing.Buffer dataclass
  * position argument in ui.abstracts.AbstractWidget class
### changed:
  * format in debug_start function
  * optimize import
  * draw method in core.terminal.Terminal class
  * build method in ui.abstracts.AbstractWidget class
  * build and add_element method in ui.abstracts.AbstractLayout class
  * event system in ui.abstracts module
  * key_pressed method in ui.board.HLayout class
### deleted:
  * \_\_getitem__ method in core.typing.Collection class