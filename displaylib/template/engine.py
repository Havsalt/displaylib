from __future__ import annotations

from .node import Node


class Engine:
    """Engine base class
    NOTE: only one Engine instance should exist per script instance
    """
    tps: int = 4
    is_running: bool = False

    def __new__(cls: type[Engine], *args, **kwargs) -> Engine:
        instance = object.__new__(cls)
        Node.root = instance
        return instance

    def __init__(self) -> None: # default implementation
        self._on_start()
        self.is_running = True
        self._main_loop()
        self._on_exit()

    def _on_start(self) -> None:
        return
    
    def _on_exit(self) -> None:
        return
    
    def _update(self, delta: float) -> None:
        return
    
    def _main_loop(self) -> None:
        def sort_fn(pair: tuple[int, Node]):
            _id, node = pair
            if getattr(node, "__logical__") == False:
                return node.z_index
            else:
                return -1 # logical nodes have by default a higher process priority (default for other nodes are 0)

        delta = 1.0 / self.tps
        nodes = tuple(Node.nodes.values())
        while self.is_running:
            self._update(delta)
            for node in nodes:
                node._update(delta)

            for node in Node._queued_nodes:
                del Node.nodes[id(node)]
            Node._queued_nodes.clear()

            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            nodes = tuple(Node.nodes.values())
