"""DisplayLib

Submodules:
- template
- ascii (default)
- pygame
"""

__version__ = "0.0.1"
__author__ = "FloatingInt"
__all__ = [
    "Vec2",
    "overload",
    "OverloadUnmatched",
    "ASCIINode",
    "ASCIIEngine",
    "ASCIISurface",
    "ASCIIClient"
]

# utility
from .overload import overload, OverloadUnmatched
from .math import Vec2
# default module
from .ascii import (
    Node as ASCIINode,
    Engine as ASCIIEngine,
    Surface as ASCIISurface,
    Client as ASCIIClient
)
