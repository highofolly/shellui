from .overloads import dataclass, field
from typing import *


@dataclass
class Buffer:
    method: Callable
    kwargs: dict = None

    def __post_init__(self):
        if self.kwargs is not None:
            for name, key in self.kwargs.items():
                setattr(self, name, key)
