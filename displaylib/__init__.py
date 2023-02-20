"""DisplayLib
----------------

Submodules:
- template
- ascii (default)
- pygame
"""

__version__ = "0.0.6"
__author__ = "FloatingInt"
__all__ = [ # when using default mode
    "Vec2",
    "overload",
    "OverloadUnmatched",
    "graphme",
    "ASCIINode",
    "ASCIIEngine",
    "ASCIICamera",
    "ASCIISurface",
    "ASCIIScreen",
    "ASCIIImage",
    "ASCIIClient",
    "Clock",
    ""
]

# -- util
from .overload import overload, OverloadUnmatched
from .math import Vec2
# -- imports
from .ascii import (
    # -- util
    grapheme as graphme,
    # -- core
    Node as ASCIINode,
    Engine as ASCIIEngine,
    Camera as ASCIICamera,
    Surface as ASCIISurface,
    Screen as ASCIIScreen,
    Image as ASCIIImage,
    Client as ASCIIClient,
    Frame as Frame,
    Animation as Animation,
    EmptyAnimation as EmptyAnimation,
    AnimationPlayer as AnimationPlayer,
    Clock as Clock,
    # -- prefab
    Label as ASCIILabel
)
