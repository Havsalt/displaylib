from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ..template.type_hints import MroNext, NodeType
from .color import RESET, WHITE
from .type_hints import ValidColorNode

if TYPE_CHECKING:
    from .color import ColorValue


class Color: # Component (mixin class)
    """`Color` mixin class for adding `colors` to a textured node class

    Requires Components:
        - `Transform2D`: uses position and rotation to place the texture
        - `Texture`: allows the node to be displayed
    """
    color: ColorValue
    
    def __new__(cls: type[NodeType], *args, color = None, **kwargs) -> NodeType:
        mro_next = cast(MroNext[ValidColorNode], super())
        instance = mro_next.__new__(cls, *args, **kwargs)
        # override -> class value -> default
        if color is not None:
            instance.color = color
        elif not hasattr(instance, "color"):
            instance.color = WHITE
        return cast(NodeType, instance)

    def _get_final_texture(self) -> list[list[str]]:
        """Applies color to the texture right before rendering. WHITE color just returns the uncolorized texture

        Returns:
            list[list[str]]: colorized texture
        """
        self = cast(ValidColorNode, self) # fixes type hints
        transparent = self.root.screen.cell_transparant
        return [
            [self.color + char + RESET if char != transparent else char for char in line]
            for line in self.texture
        ] if self.color != WHITE else self.texture
