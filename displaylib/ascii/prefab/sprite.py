from __future__ import annotations

from ...math import Vec2i
from ..node import ASCIINode2D
from ..texture import Texture


class ASCIISprite(ASCIINode2D, Texture):
    """Prefabricated `ASCIISprite`

    Components:
        `Texture`: allows the node to be displayed
    """
    
    def size(self) -> Vec2i:
        """Returns the width and height of `.texture` as a vector

        Returns:
            Vec2: size of the content
        """
        longest = len(max(self.texture, key=len))
        lines = len(self.texture)
        return Vec2i(longest, lines)
