from .. import logging
from .typings import List, Tuple, Callable, Buffer
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

        def _recursive_buffer_iteration(method: Callable, position: Tuple[int, int]) -> dict:
            method_return = method()
            if isinstance(method_return, list):
                for _bottom_buffer in method_return:
                    yield from _recursive_buffer_iteration(_bottom_buffer.method, [a + b for a, b in zip(_bottom_buffer.position, position)])
            else:
                yield {"y": position[1], "x": position[0], "args": method_return}

        for string_args in _recursive_buffer_iteration(self._buffer.method, self._buffer.position):
            self.stdscr.addstr(string_args["y"], string_args["x"], string_args["args"])
        self.stdscr.refresh()

    def read(self) -> int:
        return self.stdscr.getch()
