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

__version__ = "0.0.8"
__author__ = "Floating-Int"
__all__ = [ # default mode is used when using the star notation
    # math
    "lerp",
    "sign",
    "Vec2",
    "Vec2i",
    # utility
    "graphme",
    # standard
    "Node",
    "Node2D",
    # core ascii
    "ASCIINode2D",
    "ASCIIEngine",
    "ASCIICamera",
    "ASCIISurface",
    "ASCIIScreen",
    "ASCIIImage",
    "ASCIILabel",
    "ASCIILine",
    "ASCIISprite",
    # networking (module)
    "networking"
]

# math
from .math import lerp, sign, Vec2, Vec2i
# standard
from .template import Node, Node2D
from .ascii import (
    # utility
    grapheme as graphme, # (module)
    # ascii nodes
    Node2D as ASCIINode2D,
    Engine as ASCIIEngine,
    Camera as ASCIICamera,
    Surface as ASCIISurface,
    Screen as ASCIIScreen,
    Image as ASCIIImage,
    Frame as Frame,
    Animation as Animation,
    EmptyAnimation as EmptyAnimation,
    AnimationPlayer as AnimationPlayer,
    Clock as Clock,
    # prefabricated
    Label as ASCIILabel,
    Line as ASCIILine,
    Sprite as ASCIISprite,
    # networking
    networking # (module)
)
