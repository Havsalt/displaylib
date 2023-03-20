from __future__ import annotations

from typing import TYPE_CHECKING

from ..math import Vec2
from .node import ASCIINode2D

if TYPE_CHECKING:
    from ..template import Node

# TODO: make this a component
class ASCIISprite2D(ASCIINode2D):
    _instances: list[ASCIISprite2D] = []
    texture: list[list[str]] = []

    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index, force_sort)
        ASCIISprite2D._instances.append(self)
        self.texture: list[list[str]] = []
    
    def size(self) -> Vec2:
        """Returns the width and height of content as a vector

        Returns:
            Vec2: size of the content
        """
        longest = len(max(self.texture, key=len))
        lines = len(self.texture)
        return Vec2(longest, lines)
    
    def queue_free(self) -> None:
        """Tells the Engine to `delete` this <Node> after
        every node has been called `_update` on
        """
        if self in ASCIISprite2D._instances:
            ASCIISprite2D._instances.remove(self)
        super().queue_free()
