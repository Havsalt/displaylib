from __future__ import annotations

from typing import cast

from ..template.type_hints import MroNext, Self
from .color import RESET, WHITE, _Color
from .type_hints import ColorMixin, ValidColorNode


class Color: # Component (mixin class)
    """`Color` mixin class for adding `colors` to a textured node class

    Requires Components:
        - `Transform2D`: uses position and rotation to place the texture
        - `Texture`: allows the node to be displayed
    """
    color: _Color
    
    def __new__(cls: type[Self], *args, color: _Color = WHITE, **kwargs) -> Self:
        mro_next = cast(MroNext[ValidColorNode], super())
        instance = mro_next.__new__(cast(type[ColorMixin], cls), *args, **kwargs)
        instance.color = color
        return cast(Self, instance)

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
