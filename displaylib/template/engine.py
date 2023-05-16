from __future__ import annotations

from .node import Node


class EngineMixinSortMeta(type):
    """Engine metaclass for initializing `Engine` subclass after other `mixin` classes
    """
    @staticmethod
    def _mixin_sort(base: type) -> int:
        if base == Engine:
            return 2
        elif issubclass(base, Engine):
            return 1
        return 0

    def __new__(cls, name: str, bases: tuple[type], attrs: dict[str, object]):
        sorted_bases = tuple(sorted(bases, key=EngineMixinSortMeta._mixin_sort))
        return super().__new__(cls, name, sorted_bases, attrs)


class Engine(metaclass=EngineMixinSortMeta):
    """`Engine` base class

    Important: `Only one Engine instance should exist per script instance`

    Hooks:
        - `_on_start(self) -> None`
        - `_on_exit(self) -> None`
        - `_update(self, delta: float) -> None`
    """
    tps: int = 16
    is_running: bool = False
    per_frame_tasks = [] # list[function]

    def __new__(cls: type[Engine], *args, **kwargs) -> Engine:
        """Sets `Node.root` when an `Engine instance` is initialized 

        Args:
            cls (type[Engine]): engine object to be `root`

        Returns:
            Engine: the engine to be used in the program
        """
        instance = super().__new__(cls)
        setattr(Node, "root", instance)
        return instance

    def __init__(self) -> None: # default implementation
        self._on_start()
        self.is_running = True
        self._main_loop()
        self._on_exit()

    def _on_start(self) -> None:
        """Called when the after the engine has been created

        Override for custom functionality
        """
        ...
    
    def _on_exit(self) -> None:
        """Called when the engine is exiting successfully
        
        Override for custom functionality
        """
        ...
    
    def _update(self, delta: float) -> None:
        """Called every frame. Deltatime between frames is passes as argument `delta`

        Args:
            delta (float): deltatime between frames
        """
        ...
    
    def _main_loop(self) -> None:
        """Base implementation for `displaylib.template` mode
        """
        def sort_fn(element: tuple[int, Node]):
            return element[1].z_index
        
        while self.is_running:
            for task in self.per_frame_tasks:
                task()

            # TODO: add clock with delta, but no sleep
            delta = 1.0 / self.tps # static delta
            self._update(delta)
            for node in tuple(Node.nodes.values()):
                node._update(delta)

            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {uid: node for uid, node in sorted(Node.nodes.items(), key=sort_fn) if uid not in Node._queued_nodes}
            Node._queued_nodes.clear()
