from __future__ import annotations

from typing import TypeVar

from ...math import Vec2i
from ...util import pull
from ...template import Node
from ..node import ASCIINode2D
from ..texture import Texture

Self = TypeVar("Self")


@pull("texture")
class ASCIISprite(Texture, ASCIINode2D):
    """Prefabricated `ASCIISprite`

    Components:
        `Texture`: allows the node to be displayed
    """
    texture: list[list[str]]

    def __init__(self, parent: Node | None = None, *, x: int | float = 0, y: int | float = 0, texture: list[list[str]] = [], z_index: int = 0, force_sort: bool = True) -> None: # `z_index` pulled in `Texture`
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.z_index = z_index
        self.texture = texture
    
    def size(self) -> Vec2i:
        """Returns the width and height of `.texture` as a vector

        Returns:
            Vec2: size of the content
        """
        longest = len(max(self.texture, key=len))
        lines = len(self.texture)
        return Vec2i(longest, lines)
