from __future__ import annotations

from typing import TYPE_CHECKING

from ..template import Node2D

if TYPE_CHECKING:
    from ..math import Vec2
    from .surface import ASCIISurface


class ASCIINode2D(Node2D): # a variant of the Node2D
    """`ASCIINode2D` for representing 2D nodes
    """
    def _render(self, surface: ASCIISurface) -> None:
        ...
    
    def _on_screen_resize(self, size: Vec2) -> None:
        ...
