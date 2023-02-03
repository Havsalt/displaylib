import time
from ..template import Node, Engine
from .display import Display
from .surface import ASCIISurface


class ASCIIEngine(Engine):
    """ASCIIEngine for creating a world in ASCII graphics
    """

    def __init__(self, tps: int = 16, width: int = 16, height: int = 8) -> None:
        self.tps = tps
        self.display = Display(width, height)
        self._on_start()
        self.screen = ASCIISurface([], self.display.width, self.display.height)

        self.is_running = True
        self._main_loop()
    
    def _main_loop(self) -> None:
        def sort_fn(element):
            return element[1].z_index

        while self.is_running:
            delta = 1.0 / self.tps
            self.screen.clear()
            self._update(delta)
            nodes = tuple(Node.nodes.values())
            for node in nodes:
                node._update(delta)
            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            # render nodes onto main screen
            surface = ASCIISurface(nodes, self.display.width, self.display.height) # create a Surface from all the Nodes
            # self.screen.blit(surface, transparent=True)
            # self.screen.display()
            surface.display()
            time.sleep(delta) # TODO: implement clock
        self._on_exit()
        surface = ASCIISurface(nodes, self.display.width, self.display.height) # create a Surface from all the Nodes
        self.screen.blit(surface)
        self.screen.display()
