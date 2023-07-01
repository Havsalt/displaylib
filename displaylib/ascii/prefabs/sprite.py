from __future__ import annotations

import io
import os
import functools
from typing import TYPE_CHECKING, TypeVar

from ...math import Vec2, Vec2i
from .. import text
from ..node import AsciiNode2D
from ..texture import Texture
from ..colored import Color
from ..color import WHITE, _Color

if TYPE_CHECKING:
    from ...template import Node

Self = TypeVar("Self")


@functools.cache
def load_texture(file_path: str, /, *, fliph: bool = False, flipv: bool = False) -> list[list[str]]:
    file: io.TextIOWrapper = open(file_path, "r") # from disk
    texture = [list(line.rstrip("\n")) for line in file.readlines()]
    if fliph:
        texture = text.mapfliph(texture)
    if flipv:
        texture = text.mapfliph(texture)
    file.close()
    return texture


class AsciiSprite(Color, Texture, AsciiNode2D):
    """Prefabricated `AsciiSprite`

    Components:
        - `Texture`: allows the node to be displayed
        - `Color`: applies color to the texture
    
    Known Issues:
        - `If a file's content is changed after a texture has been loaded from that file, the change won't be reflected on next load due to the use of @functools.cache`
    """
    texture: list[list[str]] # NOTE: class texture is shared lists across instances unless .make_unique() or .as_unique()

    @classmethod
    def load(cls, file_path: str, /) -> AsciiSprite:
        """Load texture from file path as surface

        Args:
            file_path (str): file path to load from

        Raises:
            TypeError: file_path was not a string

        Returns:
            AsciiSprite: sprite give its texture from file content
        """
        if not isinstance(file_path, str):
            TypeError(f"argument 'file_path' is required to be of type 'str'. '{type(file_path).__name__}' found")
        fpath = os.path.normpath(file_path)
        texture = load_texture(fpath)
        return AsciiSprite(texture=texture)

    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, texture: list[list[str]] = [], color: _Color = WHITE, offset: Vec2 = Vec2(0, 0), centered: bool = False, z_index: int = 0, force_sort: bool = True) -> None: # `z_index` pulled in `Texture`
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.texture = self.texture or texture # uses class texture if set
        self.color = color
        self.offset = self.offset or offset.copy() # TODO: check if this has any effect
        self.centered = centered
        self.z_index = z_index
    
    def size(self) -> Vec2i:
        """Returns the width and height of `.texture` as a vector

        Returns:
            Vec2i: size of the content
        """
        longest = len(max(self.texture, key=len))
        lines = len(self.texture)
        return Vec2i(longest, lines)
