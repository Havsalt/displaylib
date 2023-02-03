from typing_extensions import Self
from ..template import Node


class ASCIINode(Node):
    cell_transparant = 0 # type used to indicate that a cell is transparent in `content`
    cell_default = " " # the default look of an empty cell
    # per instance
    visible: bool = False

    def __init__(self, owner: Self | None = None, x: int = 0, y: int = 0, z_index: int = 0) -> None:
        super().__init__(owner, x, y, z_index)
        self.visible = True
        self.content = [] # 2D array
