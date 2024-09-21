from .. import logging
from .typings import List, Buffer
import curses


class Terminal:
    def __init__(self):
        self._buffer: List[Buffer]
        self.stdscr: curses.window = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.curs_set(0)

    def set_buffer(self, buffer: Buffer) -> None:
        self._buffer = buffer

    def draw(self) -> None:
        self.stdscr.clear()

        def _recursive_buffer_iteration(buffer: Buffer) -> str:
            ret = ""
            method_return = buffer.method()
            if isinstance(method_return, list):
                for i in method_return:
                    ret += _recursive_buffer_iteration(i)
            else:
                ret += method_return
            return ret

        self.stdscr.addstr(_recursive_buffer_iteration(self._buffer))
        self.stdscr.refresh()

    def read(self) -> int:
        return self.stdscr.getch()
