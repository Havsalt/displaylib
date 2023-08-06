from __future__ import annotations

import os
from typing import TYPE_CHECKING

from ...math import Vec2
from ..node import AsciiNode2D
from ..texture import Texture, load_texture
from ..colored import Color
from ..color import WHITE

if TYPE_CHECKING:
    from ...template.type_hints import AnyNode
    from ..color import _Color


class AsciiSprite(Color, Texture, AsciiNode2D):
    """Prefabricated `AsciiSprite`

    Components:
        - `Texture`: allows the node to be displayed
        - `Color`: applies color to the texture
    
    Known Issues:
        - `If a file's content is changed after a texture has been loaded from that file, the change won't be reflected on next load due to the use of @functools.cache`
    """
    texture: list[list[str]] # NOTE: class texture is shared lists across instances unless `.make_unique()` or `.as_unique()`

    @classmethod
    def load(cls, file_path: str, /, *, fill: bool = True, fliph: bool = False, flipv: bool = False, transparent: str = " ", default: str = " ") -> AsciiSprite:
        """Loads texture from file path as sprite

        Args:
            file_path (str): file path to load from
            fill (optional, bool): fill in creeks with spaces. Defaults to True
            fliph (optional, bool): flips the texture horizontally. Defaults to False
            flipv (optional, bool): flips the texture vertically. Defaults to False
            transparent (optional, str): transparent key. Defaults to " "
            default (optional, str): replaces transparent cells with this. Defaults to " "

        Raises:
            TypeError: file_path was not a string

        Returns:
            AsciiSprite: sprite give its texture from file content
        """
        if not isinstance(file_path, str):
            TypeError(f"argument 'file_path' is required to be of type 'str'. '{type(file_path)}' found")
        fpath = os.path.normpath(file_path)
        texture = load_texture(fpath, fill=fill, fliph=fliph, flipv=flipv, transparent=transparent, default=default)
        return AsciiSprite(texture=texture)

    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, texture: list[list[str]] = [], color: _Color = WHITE, offset: Vec2 = Vec2(0, 0), centered: bool = False, z_index: int = 0, force_sort: bool = True) -> None:
        """Initializes the sprite

        Args:
            parent (AnyNode | None, optional): parent node. Defaults to None.
            x (float, optional): local x position. Defaults to 0.
            y (float, optional): local y position. Defaults to 0.
            texture (list[list[str]], optional): visible texture. Defaults to [].
            color (_Color, optional): texture color. Defaults to WHITE.
            offset (Vec2, optional): texture offset. Defaults to Vec2(0, 0).
            centered (bool, optional): whether the texture is centered. Defaults to False.
            z_index (int, optional): layer to render on. Defaults to 0.
            force_sort (bool, optional): whether to sort based on 'z_index' and 'process_priority'. Defaults to True.
        """
