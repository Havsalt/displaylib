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
>>> dl.Node2D() # will be of type AsciiNode
AsciiNode(x, y)

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
    "pull",
    "graphme",
    # standard
    "Node",
    "Node2D",
    # core ascii
    "AsciiNode2D",
    "AsciiEngine",
    "AsciiCamera",
    "AsciiSurface",
    "AsciiScreen",
    "AsciiImage",
    "AsciiLabel",
    "AsciiLine",
    "AsciiSprite",
    # networking (module)
    "networking"
]

# math
from .math import lerp, sign, Vec2, Vec2i
# utility
from .util import pull
# standard
from .template import Node, Node2D
from .ascii import (
    # utility
    grapheme as graphme, # (module)
    # ascii nodes
    Node2D as AsciiNode2D,
    Engine as AsciiEngine,
    Camera as AsciiCamera,
    Surface as AsciiSurface,
    Screen as AsciiScreen,
    Image as AsciiImage,
    Frame as Frame,
    Animation as Animation,
    EmptyAnimation as EmptyAnimation,
    AnimationPlayer as AnimationPlayer,
    AudioStreamPlayer as AudioStreamPlayer,
    Clock as Clock,
    # prefabricated
    Label as AsciiLabel,
    Line as AsciiLine,
    Sprite as AsciiSprite,
    # networking
    networking # (module)
)
