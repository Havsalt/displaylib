from typing_extensions import Self
from ..math import Vec2
from ..template import Node
from .node import ASCIINode


class ASCIICamera(Node):
    """ASCIICamera for moving the viewport
    """
    current: Self

    def __init__(self, owner: ASCIINode | None = None, x: int = 0, y: int = 0, center: bool = True, follow: bool = False) -> None:
        self.owner = owner
        self.position = Vec2(x, y)
        self.center = center # center mode only has effect if ´owner´ != None
        self.follow = follow # whether to follow the ´owner´
        self.content = [] # NOTE: attr ´content´ won't be used because ´visible´ will always be False
    
    def _update(self, delta: float) -> None:
        if self.follow and self.owner != None:
            self.global_position = self.owner.global_position

    @property
    def visible(self) -> int:
        return False # static, because it won't be displayed

    @property
    def z_index(self) -> int:
        return 0 # z_index is static, because it's required for the sort algorithm

    @property
    def z_index(self) -> int:
        return 0 # z_index static, because it's required for the sort algorithm

ASCIICamera.current = ASCIICamera() # default camera
