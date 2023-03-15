"""Pygame submodule from DisplayLib

Raises:
    ModuleNotFoundError: `pygame` was not found
"""

__all__ = [
    # -- standard
    "lerp",
    "sign",
    "Vec2",
    "Node",
    # -- core pygame
    "Node2D",
    "Engine"
]

try: # check if pygame is installed
    import pygame as _pygame
    import os as _os
    _os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
    del _os
    _pygame.init() # init without displaying message
    del _pygame
except ModuleNotFoundError as error:
    raise ModuleNotFoundError("missing external module: pygame, which is required to use this submodule") from error

# -- standard
from ..math import lerp, sign, Vec2
from ..template import Node
# -- core pygame
from .node import PygameNode2D as Node2D
from .engine import PygameEngine as Engine
