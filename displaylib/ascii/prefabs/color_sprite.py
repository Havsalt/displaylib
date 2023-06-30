from __future__ import annotations

from typing import TYPE_CHECKING

from ...math import Vec2
from ..colored import Color
from .sprite import AsciiSprite
from ..color import WHITE, _Color

if TYPE_CHECKING:
    from ...template import Node


class AsciiColorSprite(Color, AsciiSprite):
    """Prefabricated `AsciiColorSprite`

    Components:
        - `Color`: applies color to the texture
    """
    def __init__(self, parent: Node | None = None, *, x: int | float = 0, y: int | float = 0, color: _Color = WHITE, texture: list[list[str]] = [], offset: Vec2 = Vec2(0, 0), centered: bool = False, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, texture=texture, offset=offset, centered=centered, z_index=z_index, force_sort=force_sort)
        self.color = color
