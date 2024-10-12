from typing import Protocol, runtime_checkable, List, Callable, Any, Union, Tuple


@runtime_checkable
class BaseElementInterface(Protocol): ...


@runtime_checkable
class KeyboardManagerInterface(Protocol):
    parent: BaseElementInterface
    keyboard_events: List['KeyboardEvent']
    def add_keyboard_event(self, function: Callable, _lambda: Callable = lambda key_char: True) -> 'KeyboardEvent': ...
    def key_pressed(self, key_char) -> List[Any]: ...


@runtime_checkable
class FlagsManagerInterface(Protocol):
    parent: BaseElementInterface
    flags: dict
    def __getattr__(self, item): ...
    def __setattr__(self, key, value: bool): ...
    def __delattr__(self, item): ...


@runtime_checkable
class EventManagerInterface(Protocol): ...


@runtime_checkable
class CreateInterface(Protocol):
    cls: EventManagerInterface
    def __init__(self, cls: EventManagerInterface): ...
    def __getattr__(self, name: str): ...


@runtime_checkable
class CallInterface(Protocol):
    def __newattr__(self, name: str): ...


@runtime_checkable
class EventManagerInterface(Protocol):
    create: CreateInterface
    call: CallInterface
    def __init__(self, parent: object): ...


@runtime_checkable
class BaseElementInterface(Protocol):
    position: 'Position'
    size: 'Position'
    tag: str
    state: 'ElementState'
    flags: FlagsManagerInterface
    keyboard: KeyboardManagerInterface
    event: EventManagerInterface
    def select(self) -> None: ...
    def deselect(self) -> None: ...
    def set_fixed_size(self, size: Union['Position', Tuple[int, int]]) -> None: ...
    def set_floating_size(self) -> None: ...
    def get_size(self) -> 'Position': ...
    def update(self) -> Any: ...
    def render(self) -> Union[str, List['Buffer']]: ...
    def build(self) -> 'Buffer': ...
