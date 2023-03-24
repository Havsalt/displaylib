from __future__ import annotations

import os

from ..math import Vec2, Vec2i
from ..template import Node, Engine
from .clock import Clock
from .screen import ASCIIScreen
from .surface import ASCIISurface
from .camera import ASCIICamera
from .node import ASCIINode2D
from .texture import Texture


class ASCIIEngine(Engine):
    """`ASCIIEngine` for creating a world in ASCII graphics
    """

    def __new__(cls: type[ASCIIEngine], *args, **kwargs) -> Engine:
        """Sets `Node.root` when an Engine instance is initialized. Initializes default `ASCIICamera`

        Args:
            cls (type[ASCIIEngine]): engine object to be root

        Returns:
            ASCIIEngine: the engine to be used in the program
        """
        instance = super().__new__(cls)
        if not hasattr(ASCIICamera, "current"):
            camera = ASCIICamera()
            setattr(ASCIICamera, "current", camera) # initialize default camera
        return instance

    def __init__(self, tps: int = 16, width: int = 16, height: int = 8, auto_resize_screen: bool = False, screen_margin: Vec2 = Vec2(1, 1), *args, **kwargs) -> None:
        """Initialize and start the engine (only 1 instance should exist)

        Args:
            tps (int, optional): ticks per second (fps). Defaults to 16.
            width (int, optional): screen width. Defaults to 16.
            height (int, optional): screen height. Defaults to 8.
        """
        self.tps = tps
        self.auto_resize_screen = auto_resize_screen
        self.screen_margin = screen_margin # TODO: add setter/getter to force screen update
        self.screen = ASCIIScreen(width=width, height=height)
        if auto_resize_screen:
            terminal_size = os.get_terminal_size()
            if terminal_size.columns != self.screen.width or terminal_size.lines != self.screen.height:
                self.screen.width = int(terminal_size.columns - self.screen_margin.x)
                self.screen.height = int(terminal_size.lines - self.screen_margin.y)
                os.system("cls")
        super(__class__, self).__init__(*args, **kwargs)
        self._on_start()

        self.is_running = True
        self._main_loop()
    
    def _render(self, surface: ASCIISurface) -> None:
        ...
    
    def _main_loop(self) -> None:
        def sort_fn(element: tuple[int, Node]):
            return element[1].z_index

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
            
            if self.auto_resize_screen:
                terminal_size = os.get_terminal_size()
                if ((terminal_size.columns - self.screen_margin.x) != self.screen.width) or ((terminal_size.lines - self.screen_margin.y) != self.screen.height):
                    self.screen.width = int(terminal_size.columns - self.screen_margin.x)
                    self.screen.height = int(terminal_size.lines - self.screen_margin.y)
                    size = Vec2i(terminal_size.columns, terminal_size.lines)
                    for node in nodes:
                        if isinstance(node, ASCIINode2D):
                            node._on_screen_resize(size)
                    os.system("cls")
            
            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            nodes = tuple(Node.nodes.values())

            # render content of visible nodes onto a surface
            self.screen.rebuild(Texture._instances, self.screen.width, self.screen.height)
            
            self._render(self.screen)
            # nodes can render custon data onto the screen
            for node in nodes:
                if isinstance(node, ASCIINode2D):
                    node._render(self.screen)
            
            self.screen.show()
            clock.tick()
        
        # v exit protocol v
        self._on_exit()
        surface = ASCIISurface(Node.nodes.values(), self.screen.width, self.screen.height) # create a Surface from all the Nodes
        self.screen.blit(surface)
        self.screen.show()
