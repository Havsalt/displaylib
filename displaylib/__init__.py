"""# DisplayLib
----------------

An object-oriented framework for displaying ASCII graphics and creating an infinite world, aimed at simplifying the process

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
    "lerp",              # (function)
    "sign",              # (function)
    "Vec2",              # (data structure)
    "Vec2i",             # (data structure)
    # utility
    "pull",              # (class decorator)
    # core ascii
    "Node",              # (class)
    "Node2D",            # (class)
    "Engine",            # (class)
    "Camera",            # (class)
    "Screen",            # (class)
    "Frame",             # (class)
    "Animation",         # (class)
    "EmptyAnimation",    # (class)
    "AnimationPlayer",   # (class)
    "AudioStreamPlayer", # (class)
    "Clock",             # (class)
    # mixin components
    "Transform2D",       # (component)
    "Texture",           # (component)
    "Color",             # (component)
    # prefabricated
    "Label",             # (class)
    "Line",              # (class)
    "Sprite",            # (class)
    # generating colors
    "color",             # (module)
    # text alteration
    "grapheme",          # (module)
    # networking
    "networking"         # (module)
]

# ascii
from .ascii import (
    # math
    lerp,
    sign,
    Vec2,
    Vec2i,
    # utility
    pull,
    # core ascii
    Node,
    Node2D,
    Engine,
    Camera,
    Screen,
    Frame,
    Animation,
    EmptyAnimation,
    AnimationPlayer,
    AudioStreamPlayer,
    Clock,
    # mixin components
    Transform2D,
    Texture,
    Color,
    # prefabricated
    Label,
    Line,
    Sprite,
    # generating colors
    color,
    # text alteration
    grapheme,
    # networking
    networking
)
