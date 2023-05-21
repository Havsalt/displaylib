from __future__ import annotations

import os

from ..math import Vec2i
from ..template import Node, Engine
from .clock import Clock
from .screen import ASCIIScreen
from .surface import ASCIISurface
from .camera import ASCIICamera
from .node import ASCII
from .texture import Texture


class ASCIIEngine(Engine):
    """`ASCIIEngine` for creating a world in ASCII graphics

    Hooks:
        - `_render(self, surface: ASCIISurface) -> None`
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """

    def __new__(cls: type[ASCIIEngine], *args, **kwargs) -> Engine:
        """Sets `Node.root` when an Engine instance is created. Initializes default `ASCIICamera`

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

    def __init__(self, *, tps: int = 16, width: int = 16, height: int = 8, auto_resize_screen: bool = False, screen_margin: Vec2i = Vec2i(1, 1), **config) -> None:
        """Initializes and starts the engine (only 1 instance should exist)

        Args:
            tps (int, optional): ticks per second (fps). Defaults to 16.
            width (int, optional): screen width. Defaults to 16.
            height (int, optional): screen height. Defaults to 8.
            auto_resize_screen (bool, optional): whether to automatically resize the screen to fit. Defaults to False.
            screen_margin (Vec2i, optional): subtracted from os terminal size. Defaults to Vec2i(1, 1).
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
        super(__class__, self).__init__(**config)
    
    def _render(self, surface: ASCIISurface) -> None:
        """Override for custom functionality

        Args:
            surface (ASCIISurface): surface to blit onto
        """
        ...
    
    def _on_screen_resize(self, size: Vec2i) -> None:
        """Override for custom functionality

        Args:
            size (Vec2i): new terminal screen size
        """
        ...
    
    @staticmethod
    def sort_function_for_z_index(element: Texture) -> int:
        return element.z_index
    
    def _main_loop(self) -> None:
        """Overriden main loop spesific for `displaylib.ascii` mode
        """
        Node.nodes = {uid: node for uid, node in sorted(Node.nodes.items(), key=self.sort_function_for_process_priority)}
        clock = Clock(self.tps)
        while self.is_running:
            self.screen.clear()

            if self.auto_resize_screen:
                terminal_size = os.get_terminal_size()
                if ((terminal_size.columns - self.screen_margin.x) != self.screen.width) or ((terminal_size.lines - self.screen_margin.y) != self.screen.height):
                    self.screen.width = int(terminal_size.columns - self.screen_margin.x)
                    self.screen.height = int(terminal_size.lines - self.screen_margin.y)
                    size = Vec2i(terminal_size.columns, terminal_size.lines)
                    self._on_screen_resize(size)
                    for node in Node.nodes.values():
                        if isinstance(node, ASCII):
                            node._on_screen_resize(size)
                    os.system("cls")
                
            for task in self.per_frame_tasks:
                task()
            
            self._update(clock.get_delta())
            for node in Node.nodes.values():
                node._update(clock.get_delta())

            if Node._request_process_priority_sort: # only sort once per frame if needed
                for uid in Node._queued_nodes:
                    del Node.nodes[uid]
                Node._queued_nodes.clear()
                Node.nodes = {uid: node for uid, node in sorted(Node.nodes.items(), key=self.sort_function_for_process_priority)}
            if Texture._request_z_index_sort:
                Texture._instances.sort(key=self.sort_function_for_z_index)

            # render content of visible nodes onto a surface
            self.screen.rebuild(Texture._instances, self.screen.width, self.screen.height)
            
            self._render(self.screen)
            # nodes can render custom data onto the screen
            for node in Node.nodes.values():
                if isinstance(node, ASCII):
                    node._render(self.screen)
            
            self.screen.show()
            clock.tick()
        
        # v exit protocol v
        self._on_exit()
        surface = ASCIISurface(Texture._instances, self.screen.width, self.screen.height) # create a Surface from all the Nodes
        self.screen.blit(surface)
        self.screen.show()
