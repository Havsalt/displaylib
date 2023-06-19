from __future__ import annotations

import io
import os
import functools
from typing import TypeVar

from ...math import Vec2, Vec2i
from ...template import Node
from ..node import AsciiNode2D
from ..texture import Texture

Self = TypeVar("Self")


@functools.cache
def load_texture(file_path: str, /) -> list[list[str]]:
    file: io.TextIOWrapper = open(file_path, "r") # from disk
    lines = file.readlines()
    stripped = map(lambda line: line.rstrip("\n"), lines)
    texture = list(map(list, stripped))
    file.close()
    return texture


class AsciiSprite(Texture, AsciiNode2D):
    """Prefabricated `AsciiSprite`

    Components:
        - `Texture`: allows the node to be displayed
    
    Known Issues:
        - `If a file's content is changed after a texture has been loaded from that file, the change won't be reflected on next load due to the use of @functools.cache`
    """
    texture: list[list[str]] # NOTE: class texture is shared lists across instances

    @classmethod
    def load(cls, file_path: str, /) -> AsciiSprite:
        """Load texture from file path as surface

        Args:
            file_path (str): file path to load from

        Raises:
            TypeError: file_path was not a string
            ValueError: file_path did not end with the correct extension (.txt)

        Returns:
            AsciiSprite: sprite give its texture from file content
        """
        if not isinstance(file_path, str):
            TypeError(f"argument 'file_path' is required to be of type 'str'. '{type(file_path).__name__}' found")
        
        fpath = os.path.normpath(file_path)
        
        if not fpath.endswith(".txt"):
            raise ValueError("argument 'file_path' needs to end with the current extension of '" + cls.extension + "'")
        
        texture = load_texture(file_path)
        sprite = AsciiSprite(texture=texture)
        return sprite

    def __init__(self, parent: Node | None = None, *, x: int | float = 0, y: int | float = 0, texture: list[list[str]] = [], offset: Vec2 = Vec2(0, 0), centered: bool = False, z_index: int = 0, force_sort: bool = True) -> None: # `z_index` pulled in `Texture`
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.texture = self.texture or texture # uses class texture if set
        self.offset = offset
        self.centered = centered
        self.z_index = z_index
    
    def size(self) -> Vec2i:
        """Returns the width and height of `.texture` as a vector

        Returns:
            Vec2: size of the content
        """
        longest = len(max(self.texture, key=len))
        lines = len(self.texture)
        return Vec2i(longest, lines)
