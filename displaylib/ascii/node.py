from __future__ import annotations

from typing import TYPE_CHECKING

from ..template import Node2D

if TYPE_CHECKING:
    from ..math import Vec2
    from ..template import Node
    from .surface import ASCIISurface


class ASCIINode2D(Node2D): # a variant of the Node2D
    """ASCIINode for representing 2D nodes
    """
    __logical__: bool = False # exists in the "real world"

    cell_transparant: str = " " # type used to indicate that a cell is transparent in `content`
    cell_default: str = " " # the default look of an empty cell

    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index, force_sort)
        self.content: list[list[str]] = [] # 2D array
    
    def _render(self, surface: ASCIISurface) -> None:
        ...
    
    def _on_screen_resize(self, size: Vec2) -> None:
        ...
