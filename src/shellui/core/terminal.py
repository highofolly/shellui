from ..common.types import List, Union, Buffer, Position
from ..common.debug import logging
import curses


class Terminal:
    """
    Manages interface for working with text-based user interface.
    """
    def __init__(self):
        self._buffer: Buffer
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.curs_set(0)

    def set_buffer(self, buffer: Buffer) -> None:
        """
        Sets rendering buffer.

        :param buffer: Rendering buffer
        :type buffer: Buffer
        :rtype: None
        """
        self._buffer = buffer

    def draw(self) -> None:
        """
        Clears screen and draws buffer contents to the screen.

        :rtype: None
        """
        self.stdscr.clear()

        def _recursive_buffer_iteration(buffer: Buffer) -> list:
            method_return: Union[str, List[Buffer]] = buffer.function()
            if isinstance(method_return, list):
                for _bottom_buffer in method_return:
                    _bottom_buffer.position = Position(*[a + b for a, b in zip(_bottom_buffer.position, buffer.position)])
                    yield from _recursive_buffer_iteration(_bottom_buffer)
            else:
                yield [buffer.position.y, buffer.position.x, method_return]

        for string_args in _recursive_buffer_iteration(self._buffer):
            self.stdscr.addstr(*string_args)
        self.stdscr.refresh()

    def read(self) -> int:
        """
        Reads character entered by user.

        :return: Key char
        :rtype: int
        """
        return self.stdscr.getch()

    def close(self):
        """
        Closes the curses window and restores the terminal to its original state.

        :rtype: None
        """
        curses.endwin()
