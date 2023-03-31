"""## Template submodule of DisplayLib

Provides a skeleton for extending functionality

Provides both `Client` and `Server` classes for integrating networking compatible with `displaylib.template`
"""

__all__ = [
    "lerp",
    "sign",
    "Vec2",
    "Vec2i",
    "Node",
    "Node2D",
    "Engine",
    "networking" # (module)
]

from ..math import lerp, sign, Vec2, Vec2i
from .node import Node, Node2D
from .engine import Engine
from . import networking
