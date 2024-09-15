from .typings import Callable


class EventUnit:
    def __setfunc__(self, func: Callable = None):
        self.func: Callable = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class EventManager:
    def __init__(self):
        class Create:
            def __init__(self, cls: EventManager):
                self.cls = cls

            def __getattr__(self, name):
                return self.cls.call.__newattr__(name)

        class Call:
            def __newattr__(self, name):
                setattr(self, name, EventUnit())
                return getattr(self, name).__setfunc__

        self.create = Create(self)
        self.call = Call()