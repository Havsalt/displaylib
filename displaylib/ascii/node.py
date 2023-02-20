from typing_extensions import Self
from ..math import Vec2
from ..template import Node2D
from .types import ASCIISurface


class ASCIINode(Node2D): # a variant of the Node2D
    __logical__ = False # exists in the "real world"

    cell_transparant = " " # type used to indicate that a cell is transparent in `content`
    cell_default = " " # the default look of an empty cell

    def __init__(self, parent: Self | None = None, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index, force_sort)
        self.content = [] # 2D array
    
    def _render(self, surface: ASCIISurface) -> None:
        return
    
    def _resize(self, size: Vec2) -> None:
        return
