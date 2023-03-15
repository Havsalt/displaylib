"""ASCII submodule from DisplayLib
"""

__all__ = [
    # -- standard
    "lerp",
    "sign",
    "Vec2",
    "Node",
    # -- util
    "grapheme",
    # -- core ascii
    "Node2D",
    "Engine",
    "Camera",
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
from ..math import lerp, sign, Vec2
from ..template import Node
# -- util
from . import grapheme
# -- core ascii
from .node import ASCIINode2D as Node2D
from .engine import ASCIIEngine as Engine
from .camera import ASCIICamera as Camera
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
