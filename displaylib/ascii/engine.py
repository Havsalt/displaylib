from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

from ..math import Vec2i
from ..template import Node, Engine
from ..template.type_hints import MroNext, EngineType
from .clock import Clock
from .screen import AsciiScreen
from .camera import AsciiCamera
from .node import Ascii
from .texture import Texture

if TYPE_CHECKING:
    from .type_hints import ValidTextureNode


class AsciiEngine(Engine):
    """`AsciiEngine` for creating a world in Ascii graphics

    Hooks:
        - `_on_start(self) -> None`
        - `_on_exit(self) -> None`
        - `_update(self, delta: float) -> None`
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """
    auto_resize_screen: bool
    screen_margin: Vec2i
    screen: AsciiScreen

    def __new__(cls: type[EngineType], *, tps: int = 16, width: int = 16, height: int = 8, initial_clear: bool = False, auto_resize_screen: bool = False, screen_margin: Vec2i = Vec2i(1, 1), **config) -> EngineType:
        """Sets `Node.root` when an Engine instance is created. Initializes default `AsciiCamera`

        Args:
            cls (type[EngineType]): engine object to be root

        Returns:
            EngineType: the engine to be used in the program
        """
        mro_next = cast(MroNext[AsciiEngine], super())
        instance = mro_next.__new__(cls, tps=tps, **config)
        instance.tps = tps
        instance.auto_resize_screen = auto_resize_screen
        instance.screen_margin = screen_margin
        instance.screen = AsciiScreen(width=width, height=height)
        
        if auto_resize_screen:
            terminal_size = os.get_terminal_size()
            if terminal_size.columns != instance.screen.width or terminal_size.lines != instance.screen.height:
                instance.screen.width = int(terminal_size.columns - instance.screen_margin.x)
                instance.screen.height = int(terminal_size.lines - instance.screen_margin.y)
                if not initial_clear: # only clear once, so wait a bit to do it anyways
                    os.system("cls")

        if initial_clear:
            os.system("cls")

        if not hasattr(AsciiCamera, "current"):
            camera = AsciiCamera()
            AsciiCamera.current = camera # initialize default camera
        return cast(EngineType, instance)

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
        super().__init__(tps=tps)
    
    def _on_screen_resize(self, size: Vec2i) -> None:
        """Override for custom functionality

        Args:
            size (Vec2i): new terminal screen size
        """
        ...
    
    @staticmethod
    def sort_function_for_z_index(element: ValidTextureNode) -> tuple[int, int]:
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
                    self.screen.clear() # used to resize its `.texture`
                    size = Vec2i(terminal_size.columns, terminal_size.lines)
                    self._on_screen_resize(size)
                    for node in Node.nodes.values():
                        if isinstance(node, Ascii):
                            node._on_screen_resize(size)
                    os.system("cls")
                
            for task in self.per_frame_tasks:
                task() # type: ignore
            
            self._update(clock.delta_time)
            for node in tuple(Node.nodes.values()): # tuple, because removing a ref in lets say an list will free the node during iteration
                node._update(clock.delta_time)

            if Node._request_process_priority_sort: # only sort once per frame if needed
                for uid in Node._queued_nodes:
                    del Node.nodes[uid]
                Node._queued_nodes.clear()
                Node.nodes = {uid: node for uid, node in sorted(Node.nodes.items(), key=self.sort_function_for_process_priority)}
            if Texture._request_z_index_sort:
                Texture._instances.sort(key=self.sort_function_for_z_index)

            # render content of visible nodes onto a surface
            self.screen.render(Texture._instances)
            
            self.screen.show()
            clock.tick()
        
        self.screen.clear()
        self.screen.render(Texture._instances)
        self.screen.show()
        # _on_exit() is called automatically after this
