from __future__ import annotations

import os
import types

from ..math import Vec2i
from ..template import Node, Engine
from .clock import Clock
from .extensions.mouse import MouseEvent, MouseMotionEvent, get_mouse_position
from .screen import AsciiScreen
from .camera import AsciiCamera
from .node import Ascii
from .texture import Texture

class TextureNode(Texture, Node):
    """Type hint for classes deriving from: `Texture`, `Node`
    """


class AsciiEngine(Engine):
    """`AsciiEngine` for creating a world in Ascii graphics

    Hooks:
        - `_on_start(self) -> None`
        - `_on_exit(self) -> None`
        - `_update(self, delta: float) -> None`
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """

    def __new__(cls: type[AsciiEngine], *args, **kwargs) -> AsciiEngine:
        """Sets `Node.root` when an Engine instance is created. Initializes default `AsciiCamera`

        Args:
            cls (type[AsciiEngine]): engine object to be root

        Returns:
            AsciiEngine: the engine to be used in the program
        """
        instance = super().__new__(cls)
        if not hasattr(AsciiCamera, "current"):
            camera = AsciiCamera()
            setattr(AsciiCamera, "current", camera) # initialize default camera
        # # enable mouse events
        # if getattr(instance, "mouse", False) or instance.__annotations__.get("mouse", False):
        #     # setup a handler for updating the mouse
        #     def _update_mouse(self) -> None:
        #         mouse_events = []
        #         mouse_position = MouseMotionEvent(position=get_mouse_position())
        #         mouse_events.append(mouse_position)
        #         for event in mouse_events:
        #             self._on_mouse_event(event)
        #         for node in tuple(Node.nodes.values()):
        #             if isinstance(node, Ascii):
        #                 for mouse_event in mouse_events:
        #                     node._on_mouse_event(mouse_event)
        #     setattr(instance, "_update_mouse", types.MethodType(_update_mouse, instance))
        #     instance.per_frame_tasks.append(getattr(instance, "_update_mouse"))
        return instance

    def __init__(self, *, tps: int = 16, width: int = 16, height: int = 8, initial_clear: bool = False, auto_resize_screen: bool = False, screen_margin: Vec2i = Vec2i(1, 1), **config) -> None:
        """Initializes and starts the engine (only 1 instance should exist)

        Args:
            tps (int, optional): ticks per second (fps). Defaults to 16.
            width (int, optional): screen width. Defaults to 16.
            height (int, optional): screen height. Defaults to 8.
            initial_clear (bool, optional): clear the screen on start. Defaults to False.
            auto_resize_screen (bool, optional): whether to automatically resize the screen to fit. Defaults to False.
            screen_margin (Vec2i, optional): subtracted from os terminal size. Defaults to Vec2i(1, 1).
        """
        self.tps = tps
        self.auto_resize_screen = auto_resize_screen
        self.screen_margin = screen_margin # TODO: add setter/getter to force screen update
        self.screen = AsciiScreen(width=width, height=height)
        if auto_resize_screen:
            terminal_size = os.get_terminal_size()
            if terminal_size.columns != self.screen.width or terminal_size.lines != self.screen.height:
                self.screen.width = int(terminal_size.columns - self.screen_margin.x)
                self.screen.height = int(terminal_size.lines - self.screen_margin.y)
                if not initial_clear: # only clear once, so wait a bit to do it anyways
                    os.system("cls")
        if initial_clear:
            os.system("cls")
        super(__class__, self).__init__(**config)
    
    def _on_screen_resize(self, size: Vec2i) -> None:
        """Override for custom functionality

        Args:
            size (Vec2i): new terminal screen size
        """
        ...
    
    @staticmethod
    def sort_function_for_z_index(element: TextureNode) -> tuple[int, int]:
        return element.z_index, element.process_priority
    
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
                        if isinstance(node, Ascii):
                            node._on_screen_resize(size)
                    os.system("cls")
                
            for task in self.per_frame_tasks:
                task()
            
            self._update(clock.get_delta())
            for node in tuple(Node.nodes.values()): # tuple, because removing a ref in lets say an list will free the node during iteration
                node._update(clock.get_delta())

            if Node._request_process_priority_sort: # only sort once per frame if needed
                for uid in Node._queued_nodes:
                    del Node.nodes[uid]
                Node._queued_nodes.clear()
                Node.nodes = {uid: node for uid, node in sorted(Node.nodes.items(), key=self.sort_function_for_process_priority)}
            if Texture._request_z_index_sort:
                Texture._instances.sort(key=self.sort_function_for_z_index)

            # render content of visible nodes onto a surface
            self.screen.build(Texture._instances)
            
            self.screen.show()
            clock.tick()
        
        # v exit protocol v
        self._on_exit()
        self.screen.build(Texture._instances)
        self.screen.show()
