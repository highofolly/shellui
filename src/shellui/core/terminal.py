import curses
from .typings import List, Buffer


class Terminal:
    def __init__(self):
        self._buffer: List[Buffer]

    def set_buffer(self, buffer: Buffer):
        self._buffer = buffer

    def draw(self):
        stdscr = curses.initscr()

        curses.noecho()
        curses.curs_set(0)
        stdscr.clear()

        def _recursive_buffer_iteration(buffer: Buffer) -> str:
            ret = ""
            method_return = buffer.method()
            if isinstance(method_return, list):
                for i in method_return:
                    ret += _recursive_buffer_iteration(i)
            else:
                ret += method_return
            return ret

        stdscr.addstr(_recursive_buffer_iteration(self._buffer))
        stdscr.getch()
