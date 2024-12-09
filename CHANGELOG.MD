
v0.3.2 / 2024-12-09
==================

## major changes:
### added:
* elements:
  * \_\_style__ and \_\_align__ methods to AbstractLayout
* handlers:
  * set_events and call_event methods to EventManager
## minor changes:
### changed:
* elements:
  * change widgets hierarchy
  * rename flag is_fixed_size to isFixedSize
  * rename flag is_active_element to isActiveElement
* handlers:
  * rename KeyboardManager, FlagsManager and CursorHandler classes
  * rename attribute Create to Set in EventManager

v0.3.2-beta / 2024-11-24
==================

## major changes:
### added:
* inheritance of Layout class to Root class
* event_name parameter in EventUnit class
* CursorHandler handler class
* AbstractLayout interface
### fixed:
* search_elements_by_tag method in AbstractLayout class
* keyboard event call in KeyboardManager.key_pressed method

v0.3.1 / 2024-10-19
==================

## minor changes:
### updated:
* README.MD file
* requirements parameter in setup.py
* sphinx documentation
* docstring in terminal and types modules
* .readthedocs.yaml file

v0.3.1-beta.1 / 2024-10-13
==================

### added:
  * shellui.common package
  * elements:
    * flags parameter to BaseElement class
    * overload methods for set_fixed_size method
    * BaseFlags interface for BaseElement class
  * handler:
    * parent attribute to FlagsManager class
    * set_flag and get_flag methods to FlagsManager class
  * constants logging levels EVENT, KEYBOARD and CREATE
  * interface classes in common.interfaces module
  * event get_size in BaseElement class calculates size of Layouts/Widgets and is called in Layout.update method
### changed:
  * elements:
    * search_elements_by_tag method recursively accepts subelement tags
  * handler:
    * add interface methods to BaseFlags class
    * now FlagsManager class inherits dict class
  * debug:
    * debug_start method
    * move debug functions to common.debug module
  *  move EventUnit and KeyboardEvent dataclasses to common.types module
### fixed:
  * add_elements method in AbstractLayout class

v0.3.0.post1 / 2024-10-12
==================

### fixed:
  * build:
    * include README.MD, LICENSE and requirements.txt in build

v0.3.0 / 2024-10-11
==================

### added:
  * build:
    * requirements and setup configuration file in root directory
    * metadata in form of headers in shellui module
  * docs:
    * automatically created docstring documentation via sphinx in docs/ directory
### changed:
  * build:
    * list of ignored files for git in .gitignore
  * docs:
    * update item INSTALLATION in README.MD file

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