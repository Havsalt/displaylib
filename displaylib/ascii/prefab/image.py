from __future__ import annotations

import io
import os
from typing import ClassVar

from .sprite import AsciiSprite


class AsciiImage:
    """Prefabricated `AsciiImage` used to `.load()` an image from disk
    """
    extension: ClassVar[str] = ".txt"
    _cache: ClassVar[dict[str, tuple[list[list[str]], int, int]]] = {}

    @classmethod
    def load(cls, file_path: str, /, *, cache: bool = True) -> AsciiSprite:
        """Load texture from file path as surface

        Args:
            file_path (str): file path to load from
            cache (bool, optional): whether to use cached texture (if cached). Defaults to True.

        Raises:
            TypeError: file_path was not a string
            ValueError: file_path did not end with the correct extension

        Returns:
            AsciiSurface: a surface with the texture rendered onto it
        """
        if not isinstance(file_path, str):
            TypeError(f"argument 'file_path' is required to be of type 'str'. '{type(file_path).__name__}' found")
        
        fpath = os.path.normpath(file_path)
        if fpath in cls._cache and cache: # from cache
            (texture, width, height) = cls._cache[fpath]
            sprite = AsciiSprite(texture=texture)
            return sprite
        
        if not fpath.endswith(cls.extension):
            raise ValueError("argument 'file_path' needs to end with the current extension of '" + cls.extension + "'")
        
        file: io.TextIOWrapper = open(fpath, "r") # from disk
        lines = file.readlines()
        def strip_line(line: str) -> str:
            return line.rstrip("\n")
        stripped = map(strip_line, lines)
        texture = list(map(list, stripped))
        file.close()
        sprite = AsciiSprite(texture=texture)
        width = len(max(texture, key=len))
        height = len(texture)
        cls._cache[fpath] = (sprite.texture, width, height)
        return sprite
