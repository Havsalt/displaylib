"""## Pygame submodule of DisplayLib

Raises:
    ModuleNotFoundError: `pygame` was not found
"""

__all__ = [
    # math
    "lerp",              # (function)
    "sign",              # (function)
    "clamp",             # (function)
    "Vec2",              # (data structure)
    "Vec2i",             # (data structure)
    # utility
    "autorun",           # (class decorator)
    # base
    "BaseNode",          # (class alias)
    # core pygame
    "Node",              # (class)
    "Node2D",            # (class)
    "Engine",            # (class)
    # mixin components
    "Transform2D",       # (component)
    # networking
    "networking",        # (module)
    # typing support
    "AnyNode"            # (protocol)
]

try: # check if pygame is installed
    import os as _os
    _os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import pygame as _pygame
    if not _pygame.get_init():
        _pygame.init()
    del _os, _pygame
except ModuleNotFoundError as error:
    raise ModuleNotFoundError("missing external module: pygame, which is required to use this submodule") from error

# math
from ..math import lerp, sign, clamp, Vec2, Vec2i
# utility
from ..util import autorun
# base
from ..template import Node as BaseNode
# core pygame
from .node import PygameNode as Node, PygameNode2D as Node2D
from .engine import PygameEngine as Engine
# mixin components
from ..template import Transform2D
# networking
from ..template import networking
# typing support
from ..template.type_hints import AnyNode
