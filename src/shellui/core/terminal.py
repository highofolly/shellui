from . import List, Callable, Buffer, Position
from .. import logging
import curses


class Terminal:
    """
    Manages interface for working with text-based user interface
    """
    def __init__(self):
        self._buffer: Buffer
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.curs_set(0)

    def set_buffer(self, buffer: Buffer) -> None:
        """
        Sets rendering buffer

        :param buffer: Rendering buffer
        """
        self._buffer = buffer

    def draw(self) -> None:
        """
        Clears screen and draws buffer contents to the screen
        """
        self.stdscr.clear()

        def _recursive_buffer_iteration(method: Callable, position: Position) -> list:
            method_return = method()
            if isinstance(method_return, list):
                for _bottom_buffer in method_return:
                    yield from _recursive_buffer_iteration(_bottom_buffer.function, Position(*[a + b for a, b in zip(_bottom_buffer.position, position)]))
            else:
                yield [position.y, position.x, method_return]

        for string_args in _recursive_buffer_iteration(self._buffer.function, self._buffer.position):
            self.stdscr.addstr(*string_args)
        self.stdscr.refresh()

    def read(self) -> int:
        """
        Reads character entered by user

        :return: Key char
        """
        return self.stdscr.getch()
