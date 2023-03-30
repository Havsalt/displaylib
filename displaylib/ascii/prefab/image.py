from __future__ import annotations

import io
import os

from ..surface import ASCIISurface
from .sprite import ASCIISprite


class ASCIIImage:
    extension = ".txt"
    _cache = {}

    @classmethod
    def load(cls, file_path: str, cache: bool = True) -> ASCIISurface:
        if not isinstance(file_path, str):
            TypeError(f"argument 'file_path' is required to be of type 'str'. '{type(file_path).__name__}' found")
        fpath = os.path.normpath(file_path)
        if fpath in cls._cache and cache:
            return cls._cache[fpath]
        if not fpath.endswith(cls.extension):
            raise ValueError("argument 'file_path' needs to end with the current extension of '" + cls.extension + "'")
        file: io.TextIOWrapper = open(fpath, "r")
        texture = list(map(list, file.readlines()))
        file.close()
        node = ASCIISprite().where(texture=texture)
        cls._cache[fpath] = node
        width = len(max(texture, key=len))
        height = len(texture)
        return ASCIISurface(nodes=[node], width=width, height=height)
