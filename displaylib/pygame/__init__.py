"""## Pygame submodule of DisplayLib

Raises:
    ModuleNotFoundError: `pygame` was not found
"""

__all__ = [
    # math
    "lerp",
    "sign",
    "Vec2",
    "Vec2i",
    # standard
    "Node",
    # core pygame
    "Node2D",
    "Engine",
    # networking
    "networking"
]

try: # check if pygame is installed
    import contextlib as _contextlib
    with _contextlib.redirect_stdout(None):
        import pygame as _pygame
    _pygame.init() # init without displaying message
    del _contextlib, _pygame
except ModuleNotFoundError as error:
    raise ModuleNotFoundError("missing external module: pygame, which is required to use this submodule") from error

# math
from ..math import lerp, sign, Vec2, Vec2i
# standard
from ..template import Node
# core pygame
from .node import PygameNode2D as Node2D
from .engine import PygameEngine as Engine
# networking
from . import networking
