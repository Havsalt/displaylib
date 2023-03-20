"""## ASCII submodule of DisplayLib

Provides a framework for creating 2D worlds in ASCII
"""

__all__ = [
    # -- standard
    "lerp",
    "sign",
    "Vec2",
    "Vec2i",
    "Node",
    # -- util
    "grapheme",
    # -- core ascii
    "Node2D",
    "Engine",
    "Camera2D",
    "Screen",
    "Surface",
    "Image",
    "Client",
    "Frame",
    "Animation",
    "EmptyAnimation",
    "AnimationPlayer",
    "Clock",
    # -- prefab
    "Label",
    "Line"
]

# -- standard
from ..math import lerp, sign, Vec2, Vec2i
from ..template import Node
# -- util
from . import grapheme
# -- core ascii
from .node import ASCIINode2D as Node2D
from .engine import ASCIIEngine as Engine
from .camera import ASCIICamera2D as Camera2D
from .surface import ASCIISurface as Surface
from .screen import ASCIIScreen as Screen
from .image import ASCIIImage as Image
from .client import ASCIIClient as Client
from .animation import Frame, Animation, EmptyAnimation, AnimationPlayer
from .clock import Clock
# -- prefab
from .prefab.label import ASCIILabel as Label
from .prefab.line import ASCIILine as Line


# -- activate ANSI escape codes
import os as _os
_os.system("")
# _os.system("cls") # used when developing
del _os
