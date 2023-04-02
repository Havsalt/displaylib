from __future__ import annotations

import pygame

from ..template import Node, Engine
from .constants import DEFAULT, MILLISECOND
from .node import PygameNode2D


class PygameEngine(Engine):
    """`ASCIIEngine` for creating a world in Pygame graphics
    
    Hooks:
        - `_input(self, event: pygame.event.Event) -> None`
        - `_render(self, surface: pygame.Surface) -> None`
    """ # TODO: add hook for screen size changed
    bg_color = (255, 255, 255) # white

    def __init__(self, window_name: str = "DisplayLib Window", tps: int = 60, width: int = 512, height: int = 256, icon_path: str | None = None, flags: int = DEFAULT) -> None:
        """Initializes and starts the engine (only 1 instance should exist)

        Args:
            window_name (str, optional): name of the pygame window. Defaults to "DisplayLib Window".
            tps (int, optional): ticks per second (fps). Defaults to 60tps.
            width (int, optional): screen width. Defaults to 512px.
            height (int, optional): screen height. Defaults to 256px.
            icon_path (str | None, optional): optional icon path for setting custom icon. Defaults to None.
            flags (int, optional): pygame flags. Defaults to DEFAULT.
        """
        self._window_name = window_name
        pygame.display.set_caption(window_name)
        self.tps = tps
        self._width = width
        self._height = height
        self.icon_img: None | pygame.Surface = None
        if icon_path:
            self.icon_img = pygame.image.load(icon_path)
            pygame.display.set_icon(self.icon_img)
        self.flags = flags
        self.screen = pygame.display.set_mode(size=(width, height), flags=flags)
        self._on_start()
        
        self.is_running = True
        self._main_loop()
    
    @property
    def window_name(self) -> str:
        return self.window_name

    @window_name.setter
    def window_name(self, name: str) -> None:
        self._window_name = name
        pygame.display.set_caption(name)
    
    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, value: int) -> None: # TODO: queue this action
        self._height = value
        self.screen = pygame.display.set_mode(size=(self.width, self.height), flags=self.flags)
    
    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, value: int) -> None: # TODO: queue this action
        self._width = value
        self.screen = pygame.display.set_mode(size=(self.width, self.height), flags=self.flags)

    @property
    def icon(self) -> pygame.Surface | None:
        return self.icon_img
    
    @icon.setter
    def icon(self, icon_path: str) -> None:
        self.icon_img = pygame.image.load(icon_path)
        pygame.display.set_icon(self.icon_img)

    def _input(self, event: pygame.event.Event) -> None:
        """Override this base implementation for custom functionality

        Args:
            event (pygame.event.Event): event received
        """
        if event.type == pygame.QUIT:
            self.is_running = False
    
    def _render(self, surface: pygame.Surface) -> None:
        """Override for custom functionality

        Args:
            surface (pygame.Surface): surface to manipulate
        """
        ...
    
    def _main_loop(self) -> None:
        """Overriden main loop spesific for `displaylib.ascii` mode
        """
        def sort_fn(element: tuple[int, Node]):
            return element[1].z_index

        nodes = tuple(Node.nodes.values())
        clock = pygame.time.Clock()
        delta = 0.0
        # update one time at the very start
        self.screen.fill(self.bg_color)
        pygame.display.flip()
        while self.is_running:
            self.screen.fill(self.bg_color)
            
            for event in pygame.event.get():
                self._input(event)
                for node in nodes:
                    if isinstance(node, PygameNode2D):
                        node._input(event)
            
            self._update(delta)
            for node in nodes:
                node._update(delta)

            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            
            self._render(self.screen)
            for node in nodes: # render nodes onto the display
                if isinstance(node, PygameNode2D):
                    node._render(self.screen)
            
            pygame.display.flip()
            delta = clock.tick(self.tps) / MILLISECOND # milliseconds -> seconds
        self._on_exit()
