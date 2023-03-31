"""## ASCII submodule of DisplayLib

Provides a framework for creating 2D worlds in ASCII
"""

__all__ = [
    # math
    "lerp",
    "sign",
    "Vec2",
    "Vec2i",
    # standard
    "Node",
    # utility
    "grapheme", # (module)
    # core ascii
    "Node2D",
    "Engine",
    "Camera",
    "Screen",
    "Surface",
    "Frame",
    "Animation",
    "EmptyAnimation",
    "AnimationPlayer",
    "Clock",
    # mixin classes
    "Texture",
    # prefabricated
    "Image",
    "Label",
    "Line",
    "Sprite",
    # networking (module)
    "networking"
]

# math
from ..math import lerp, sign, Vec2, Vec2i
# standard
from ..template import Node
# utility
from . import grapheme
# core ascii
from .node import ASCIINode2D as Node2D
from .engine import ASCIIEngine as Engine
from .camera import ASCIICamera as Camera
from .surface import ASCIISurface as Surface
from .screen import ASCIIScreen as Screen
from .animation import Frame, Animation, EmptyAnimation, AnimationPlayer
from .clock import Clock
# mixin classes
from .texture import Texture
# prefabricated
from .prefab.image import ASCIIImage as Image
from .prefab.label import ASCIILabel as Label
from .prefab.line import ASCIILine as Line
from .prefab.sprite import ASCIISprite as Sprite
# networking
from . import networking


# -- activate ANSI escape codes
import os as _os
_os.system("")
# _os.system("cls") # used when developing
del _os
