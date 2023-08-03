from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from .node import Node
from .type_hints import MroNext, EngineType

if TYPE_CHECKING:
    from functools import partial
    from .type_hints import AnyNode


class EngineMixinSortMeta(type):
    """Engine metaclass for initializing `Engine` subclass after other `mixin` classes
    """
    @staticmethod
    def _mixin_sort(base: type) -> int:
        if base is Engine:
            return 2
        elif issubclass(base, Engine):
            return 1
        return 0

    def __new__(cls, name: str, bases: tuple[type], attrs: dict[str, object]):
        sorted_bases = tuple(sorted(bases, key=EngineMixinSortMeta._mixin_sort))
        return super().__new__(cls, name, sorted_bases, attrs)


class Engine(metaclass=EngineMixinSortMeta):
    """`Engine` base class

    Important: `Only 1 Engine instance should exist per script instance`

    Hooks:
        - `_on_start(self) -> None`
        - `_on_exit(self) -> None`
        - `_update(self, delta: float) -> None`
    """
    tps: int
    is_running: bool
    per_frame_tasks: list[function | partial[Any]]

    def __new__(cls: type[EngineType], *, tps: int = 16, **_overflow) -> EngineType:
        """Sets `Node.root` when an `Engine instance` is initialized 

        Args:
            cls (type[EngineType]): engine object to be `.root`.
            tps (int, optional): ticks per second. Defaults to 16.

        Returns:
            EngineType: the engine to be used in the program
        """
        mro_next = cast(MroNext[Engine], super())
        instance = mro_next.__new__(cls)
        Node.root = cast(Engine, instance)
        instance.tps = tps
        instance.is_running = False
        instance.per_frame_tasks = []
        return cast(EngineType, instance)

    def __init__(self, tps: int = 16) -> None:
        """Base implementation for initializing and running the App instance

        Args:
            tps (int, optional): ticks per second. Defaults to 16.
        """
        self.tps = tps
        self._on_start()
        self.is_running = True
        self._main_loop()
        self._on_exit()

    def _on_start(self) -> None:
        """Called after the engine has been created

        Override for custom functionality
        """
        ...
    
    def _on_exit(self) -> None:
        """Called when the engine is exiting successfully
        
        Override for custom functionality
        """
        ...
    
    def _update(self, delta: float) -> None:
        """Called every frame. Deltatime between frames is passed as argument `delta`

        Args:
            delta (float): deltatime between frames
        """
        ...
    
    @staticmethod
    def sort_function_for_process_priority(elements: tuple[str, AnyNode]) -> int:
        return elements[1].process_priority
    
    def _main_loop(self) -> None:
        """Base implementation for `displaylib.template` mode
        """
        Node.nodes = {uid: node for uid, node in sorted(Node.nodes.items(), key=self.sort_function_for_process_priority)}
        while self.is_running:
            for task in self.per_frame_tasks:
                task() # type: ignore

            # TODO: add clock with delta, but no sleep
            delta = 1.0 / self.tps # static delta
            self._update(delta)
            for node in tuple(Node.nodes.values()):
                node._update(delta)

            if Node._request_process_priority_sort: # only sort once per frame if needed
                Node._request_process_priority_sort = False
                for uid in Node._queued_nodes: # list should not contain duplicants
                    del Node.nodes[uid]
                Node._queued_nodes.clear()
                Node.nodes = {uid: node for uid, node in sorted(Node.nodes.items(), key=self.sort_function_for_process_priority)}
        # _on_exit() is called automatically after this
