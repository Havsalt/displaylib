from __future__ import annotations

import io
import os
from typing import ClassVar

from ..surface import ASCIISurface
from .sprite import ASCIISprite


class ASCIIImage:
    """Prefabricated `ASCIIImage` used to `.load()` an image from disk
    """
    extension: ClassVar[str] = ".txt"
    _cache: ClassVar[dict[str, tuple[list[list[str]], int, int]]] = {}

    @classmethod
    def load(cls, file_path: str, /, *, cache: bool = True) -> ASCIISurface:
        """Load texture from file path as surface

        Args:
            file_path (str): file path to load from
            cache (bool, optional): whether to use cached texture (if cached). Defaults to True.

        Raises:
            TypeError: file_path was not a string
            ValueError: file_path did not end with the correct extension

        Returns:
            ASCIISurface: a surface with the texture rendered onto it
        """
        if not isinstance(file_path, str):
            TypeError(f"argument 'file_path' is required to be of type 'str'. '{type(file_path).__name__}' found")
        
        fpath = os.path.normpath(file_path)
        if fpath in cls._cache and cache: # from cache
            (texture, width, height) = cls._cache[fpath]
            sprite = ASCIISprite().where(texture=texture)
            surface = ASCIISurface(nodes=[sprite], width=width, height=height)
            sprite.queue_free()
            return surface
        
        if not fpath.endswith(cls.extension):
            raise ValueError("argument 'file_path' needs to end with the current extension of '" + cls.extension + "'")
        
        file: io.TextIOWrapper = open(fpath, "r") # from disk
        texture = list(map(list, file.readlines()))
        file.close()
        sprite = ASCIISprite().where(texture=texture)
        width = len(max(texture, key=len))
        height = len(texture)
        cls._cache[fpath] = (sprite.texture, width, height)
        surface = ASCIISurface(nodes=[sprite], width=width, height=height)
        sprite.queue_free()
        return surface
