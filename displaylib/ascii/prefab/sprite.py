from __future__ import annotations

from ...math import Vec2
from ..node import ASCIINode2D
from ..texture import Texture


class ASCIISprite(ASCIINode2D, Texture):
    """Prefabricated `ASCIISprite`

    Components:
        Texture: allows the node to be displayed
    """
    
    def size(self) -> Vec2:
        """Returns the width and height of content as a vector

        Returns:
            Vec2: size of the content
        """
        longest = len(max(self.texture, key=len))
        lines = len(self.texture)
        return Vec2(longest, lines)
