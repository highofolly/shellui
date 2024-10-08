
v0.3.0-beta.1 / 2024-10-10
==================

### added:
  * widgets:
    * CheckBox class in ui.board module
  * layouts:
    * ui.board module:
      * HLayout class represents horizontal layout
      * Layout class represents abstract class of layout for layouts:
        * set_text method calculates size of text attribute
        * render method replaces element render methods with custom style method
        * set_cursor_skin method defines cursor skin
    * ui.abstracts.AbstractLayout.search_element_by_tag method searches elements in this Layout by tag
  * logging:
    * \_\_init__ module:
      * add EVENT, KEYBOARD and CREATE logging level
      * create_level method is used to create logging levels
      * logging_level argument defines logging level in debug_start function
      * save_critical_error argument in debug_start function defines whether errors will be intercepted and saved to file
  * close method calls function endwin of curses in core.terminal.Terminal class
  * add tag attribute to ui.abstracts.BaseElement class
### changed:
  * widgets:
    * text argument from Label and Button classes moved to Widget class
  * layouts:
    * ui.abstracts.AbstractLayout.add_elements method:
      * calculates size of layout by elements
      * accepts unlimited elements number
    * ui.board module:
      * common methods of VLayout class moving to Layout class
      * inheritance of select and deselect method in VLayout class
  * render:
    * board.VLayout class:
      * deselect widgets works correctly in update method
    * draw method has become more readable in core.terminal.Terminal class
  * typing:
    * typings.Collection class can pass list to parameters
### removed:
  * overridden add_elements method in ui.board.VLayout class

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