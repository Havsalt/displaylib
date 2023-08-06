"""## Pygame submodule of DisplayLib

Raises:
    ModuleNotFoundError: `pygame` was not found
"""

__all__ = [
    # math
    "lerp",              # (function)
    "sign",              # (function)
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
    "AnyNode",           # (protocol)
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
