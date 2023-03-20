from __future__ import annotations

from typing import TYPE_CHECKING

from ..math import Vec2i
from ..template import Node, Node2D

if TYPE_CHECKING:
    from .surface import ASCIISurface


class ASCIICamera2D(Node2D):
    """`ASCIICamera` for moving the viewport
    """
    FIXED = 1
    CENTERED = 3
    INCLUDE_SIZE = 5
    CENTERED_AND_INCLUDE_SIZE = 8
    current: ASCIICamera2D

    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, *, follow: bool = False, mode: int = FIXED) -> None:
        self._z_index = 0 # required in <Node2D>.__init__
        super().__init__(parent, x, y, -1, True) # TODO: move z_index into some config (the "-1" part)
        self.mode = mode # `centered` mode only has effect if `parent` != None
        self.follow = follow # whether to follow the `parent`
    
    def _render(self, surface: ASCIISurface) -> None:
        ...

    def _on_screen_resize(self, size: Vec2i) -> None:
        ...
