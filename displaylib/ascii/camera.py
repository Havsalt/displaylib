from __future__ import annotations

from typing import TYPE_CHECKING

from ..math import Vec2
from ..template import Node2D
from .types import ModeFlags

if TYPE_CHECKING:
    from .node import ASCIINode
    from .surface import ASCIISurface


class ASCIICamera(Node2D):
    """ASCIICamera for moving the viewport
    """
    __logical__: bool = True # does still "exists in the world"

    FIXED = 1
    CENTERED = 3
    INCLUDE_SIZE = 5
    CENTERED_AND_INCLUDE_SIZE = 8
    current: ASCIICamera = None

    def __init__(self, parent: ASCIINode | None = None, x: int = 0, y: int = 0, follow: bool = False, mode: ModeFlags = FIXED) -> None:
        super().__init__(parent, x, y, self.logical_z_index_default, True) # TODO: move z_index into some config (the "-1" part)
        self.mode = mode # `centered` mode only has effect if ´owner´ != None
        self.follow = follow # whether to follow the ´owner´
    
    def _update(self, delta: float) -> None:
        if self.follow and self.parent != None:
            self.global_position = self.parent.global_position
    
    def _render(self, surface: ASCIISurface) -> None:
        ...

    def _on_screen_resize(self, size: Vec2) -> None:
        ...
