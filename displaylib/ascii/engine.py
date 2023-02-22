from typing_extensions import Self
from ..template import Node, Engine
from .clock import Clock
from .screen import ASCIIScreen
from .surface import ASCIISurface
from .camera import ASCIICamera


class ASCIIEngine(Engine):
    """ASCIIEngine for creating a world in ASCII graphics
    """

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        """Set `self` as root. Initialize default camera
        """
        instance = super().__new__(cls)
        if ASCIICamera.current == None:
            ASCIICamera.current = ASCIICamera() # initialize default camera
        return instance

    def __init__(self, tps: int = 16, width: int = 16, height: int = 8) -> None:
        """Initialize and start the engine (only 1 instance should exist)

        Args:
            tps (int, optional): ticks per second (fps). Defaults to 16.
            width (int, optional): screen width. Defaults to 16.
            height (int, optional): screen height. Defaults to 8.
        """
        self.tps = tps
        self.screen = ASCIIScreen(width=width, height=height)
        self.display = ASCIISurface(Node.nodes.values()) # display is rendered onto screen
        self._on_start()

        self.is_running = True
        self._main_loop()
    
    def _render(self, surface: ASCIISurface) -> None:
        return
    
    def _main_loop(self) -> None:
        def sort_fn(pair: tuple[int, Node]):
            _id, node = pair
            if getattr(node, "__logical__") == False:
                return node.z_index
            else:
                return -1 # logical nodes have by default a higher process priority (default for other nodes are 0)

        nodes = tuple(Node.nodes.values())
        clock = Clock(self.tps)
        while self.is_running:
            delta = 1.0 / self.tps
            self.screen.clear()
            
            self._update(delta)
            for node in nodes:
                node._update(delta)

            for node in Node._queued_nodes:
                del Node.nodes[id(node)]
            Node._queued_nodes.clear()
            
            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            nodes = tuple(Node.nodes.values())

            # render content of visible nodes onto a surface
            self.display = ASCIISurface(Node.nodes.values(), self.screen.width, self.screen.height) # create a Surface from all the Nodes
            self.screen.blit(self.display, transparent=True)
            
            self._render(self.screen)
            # render nodes onto main screen
            for node in nodes:
                if getattr(node, "__logical__") == True:
                    continue
                node._render(self.screen)
            
            self.screen.show()
            clock.tick()
        
        # v exit protocol v
        self._on_exit()
        surface = ASCIISurface(Node.nodes.values(), self.screen.width, self.screen.height) # create a Surface from all the Nodes
        self.screen.blit(surface)
        self.screen.show()
