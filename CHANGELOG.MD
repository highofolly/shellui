
v0.3.0-alpha.1 / 2024-10-06
==================

### added:
  * core.handler module:
    * keyboardEvent class
    * KeyboardManager class
    * FlagsManager class
  * ui.board.Widget class
  * core.typings.Position dataclass
  * interface_level argument in core.typings.Collection class
### changed:
  * core.terminal.Terminal:
    * optimize draw method
    * rename argument console to terminal
  * methods in BaseElement class
  * methods in core.typings.Collection class
  * rename HLayout to VLayout class
### removed:
  * core.typings.Buffer class:
    * __post_init__ method
    * kwargs argument
  * ActiveWidget and StaticWidget class in ui.board module