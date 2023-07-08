from __future__ import annotations

from typing import TypeVar

from .texture import Texture
from .color import RESET, WHITE, _Color

Self = TypeVar("Self")


class Color: # Component (mixin class)
    """`Color` mixin class for adding `colors` to a textured node class

    Requires Components:
        - `Transform2D`: uses position and rotation to place the texture
        - `Texture`: allows the node to be displayed
    """
    color: _Color
    
    def __new__(cls: type[Self], *args, color: _Color = WHITE, **kwargs) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        if not isinstance(instance, Texture):
            raise TypeError(f"class '{__class__.__qualname__}' is required to derive from 'Texture' as it derives from 'Color'")
        setattr(instance, "color", color)
        return instance

    def _get_final_texture(self) -> list[list[str]]:
        """Applies color to the texture right before rendering. WHITE color just returns the uncolorized texture

        Returns:
            list[list[str]]: colorized texture
        """
        transparent = getattr(self, "root").screen.cell_transparant
        return [
            [self.color + char + RESET if char != transparent else char for char in line]
            for line in getattr(self, "texture")
        ] if self.color != WHITE else getattr(self, "texture")
