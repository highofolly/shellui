from . import Callable
from .. import logging


class EventUnit:
    def __init__(self, parent):
        self.parent: object = parent

    def __setfunc__(self, func: Callable = None):
        self.func: Callable = func

    def __call__(self, *args, **kwargs):
        args_str = ', '.join(repr(arg) for arg in args[:2]) or None
        if len(args) > 2:
            args_str += ', ...'

        kwargs_items = list(kwargs.items())
        kwargs_str = ', '.join(f'{key}: {repr(value)}' for key, value in kwargs_items[:2]) or None
        if len(kwargs_items) > 2:
            kwargs_str += ', ...'

        logging.debug(f"CLASS <{self.parent.__class__.__name__}> CALLS <{self.func.__name__}> (agrs={args_str}, kwargs={kwargs_str})")
        return self.func(*args, **kwargs)


class EventManager:
    def __init__(self, parent):
        class Create:
            def __init__(self, cls: EventManager):
                self.cls = cls

            def __getattr__(self, name):
                return self.cls.call.__newattr__(name)

        class Call:
            def __newattr__(self, name):
                setattr(self, name, EventUnit(parent))
                return getattr(self, name).__setfunc__

        self.create = Create(self)
        self.call = Call()
