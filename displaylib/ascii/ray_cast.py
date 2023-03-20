from __future__ import annotations

from typing import TYPE_CHECKING
from ..math import Vec2
from ..template import Node2D

if TYPE_CHECKING:
    from ..template import Node


class RayCast2D(Node2D): # TODO: implement
    __logical__: bool = True

    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, target_position: Vec2 = Vec2(10, 0), z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index, force_sort)
        self.target_position = target_position
    
    def is_colliding(self) -> bool:
        pass
    
    def get_collider(self) -> any:
        ...