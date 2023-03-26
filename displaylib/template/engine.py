from __future__ import annotations

from .node import Node


class EngineMixinSortMeta(type):
    """Engine metaclass for initializing `Engine` subclass after other `mixin` classes
    """
    @staticmethod
    def _mixin_sort(base: type) -> bool:
        return issubclass(base, Engine)

    def __new__(cls, name: str, bases: tuple[type], attrs: dict[str, object]):
        sorted_bases = tuple(sorted(bases, key=EngineMixinSortMeta._mixin_sort))
        return super().__new__(cls, name, sorted_bases, attrs)


class Engine(metaclass=EngineMixinSortMeta):
    """Engine base class
    NOTE: only one Engine instance should exist per script instance
    """
    tps: int = 4
    is_running: bool = False

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

    def __init__(self, *args, **kwargs) -> None: # default implementation
        super(__class__, self).__init__(*args, **kwargs)
        self._on_start()
        self.is_running = True
        self._main_loop()
        self._on_exit()

    def _on_start(self) -> None:
        ...
    
    def _on_exit(self) -> None:
        ...
    
    def _update(self, delta: float) -> None:
        ...
    
    def _main_loop(self) -> None:
        def sort_fn(element: tuple[int, Node]):
            return element[1].z_index
        
        delta = 1.0 / self.tps # TODO: implement default clock
        nodes = tuple(Node.nodes.values())
        while self.is_running:
            self._update(delta)
            for node in nodes:
                node._update(delta)

            for node in Node._queued_nodes:
                del Node.nodes[node.uid]
            Node._queued_nodes.clear()

            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            nodes = tuple(Node.nodes.values())
