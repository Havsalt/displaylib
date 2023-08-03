"""## Template submodule of DisplayLib

Provides a skeleton for extending functionality

Provides both `Client` and `Server` classes for integrating networking compatible with `displaylib.template`
"""

__all__ = [
    # math
    "lerp",             # (function)
    "sign",             # (function)
    "Vec2",             # (data structure)
    "Vec2i",            # (data structure)
    # utility
    "autorun",          # (class decorator)
    # core ascii
    "Node",             # (class)
    "Node2D",           # (class)
    "Engine",           # (class)
    # mixin components
    "Transform2D",      # (component)
    # networking
    "networking",        # (module)
    # typing support
    "AnyNode"            # (protocol)
]

# math
from ..math import lerp, sign, Vec2, Vec2i
# utility
from ..util import autorun
# core template
from .node import Node
from .node2d import Node2D
from .engine import Engine
# mixin components
from .transform import Transform2D
# networking
from . import networking
# typing support
from .type_hints import AnyNode
