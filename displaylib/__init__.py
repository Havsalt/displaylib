"""# DisplayLib
----------------

`Requires Python version >= 3.10`

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
    "lerp",
    "sign",
    "Vec2",
    "Vec2i",
    "graphme",
    "Node",
    "Node2D",
    "ASCIINode2D",
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
from .math import lerp, sign, Vec2, Vec2i
# -- standard
from .template import Node, Node2D
# -- imports
from .ascii import (
    # -- util
    grapheme as graphme,
    # -- core
    Node2D as ASCIINode2D,
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
