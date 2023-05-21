from __future__ import annotations

from typing import TYPE_CHECKING

from ..template import Node, Node2D

if TYPE_CHECKING:
    from ..math import Vec2i
    from .engine import ASCIIEngine
    from .surface import ASCIISurface


class ASCII: # mode class with common hooks
    """`ASCII` class that enables common hooks for the `ascii` mode

    Hooks:
        - `_render(self, surface: ASCIISurface) -> None`
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """
    root: ASCIIEngine

    def _render(self, surface: ASCIISurface) -> None:
        """Override for custom functionality

        Args:
            surface (ASCIISurface): surface to blit other surfaces onto
        """
        ...
    
    def _on_screen_resize(self, size: Vec2i) -> None:
        """Override for custom functionality

        Args:
            size (Vec2i): new screen size
        """
        ...


class ASCIINode(ASCII, Node): # a variant of the Node
    """`ASCIINode` with additional hooks related to `ascii` mode functionality

    Hooks:
        - `_render(self, surface: ASCIISurface) -> None`
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """


class ASCIINode2D(ASCII, Node2D): # a variant of the Node2D
    """`ASCIINode2D` with additional hooks related to `ascii` mode functionality

    Hooks:
        - `_render(self, surface: ASCIISurface) -> None`
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """
