"""DisplayLib
----------------

Requires Python version >= 3.10

----------------
Submodules:
- template
- ascii (default)
- pygame

----------------
Example using submodules to set mode:
>>> import displaylib.ascii as dl
>>> dl.Node2D() # will be of type ASCIINode
ASCIINode(x, y)

>>> import displaylib.pygame as dl
>>> dl.Node2D() # will be of type PygameNode
PygameNode(x, y)
"""

__version__ = "0.0.7"
__author__ = "FloatingInt"
__all__ = [ # when using default mode
    "Vec2",
    "graphme",
    "ASCIINode",
    "ASCIIEngine",
    "ASCIICamera",
    "ASCIISurface",
    "ASCIIScreen",
    "ASCIIImage",
    "ASCIIClient",
    "ASCIILabel",
    "ASCIILine"
]

# -- util
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
    Label as ASCIILabel,
    Line as ASCIILine
)
