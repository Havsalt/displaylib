"""## Ascii submodule of DisplayLib

Provides a framework for creating 2D worlds in Ascii
"""

__all__ = [
    # math
    "lerp",
    "sign",
    "Vec2",
    "Vec2i",
    # utility
    "pull",
    "grapheme", # (module)
    # core ascii
    "Node",
    "Node2D",
    "Engine",
    "Camera",
    "Screen",
    "Surface",
    "Frame",
    "Animation",
    "EmptyAnimation",
    "AnimationPlayer",
    "AudioStreamPlayer",
    "Clock",
    # mixin classes
    "Transform2D",
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
# utility
from ..util import pull
from . import grapheme
# core ascii
from .node import AsciiNode as Node, AsciiNode2D as Node2D
from .engine import AsciiEngine as Engine
from .camera import AsciiCamera as Camera
from .surface import AsciiSurface as Surface
from .screen import AsciiScreen as Screen
from .animation import Frame, Animation, EmptyAnimation, AnimationPlayer
from .audio import AudioStreamPlayer
from .clock import Clock
# mixin classes
from ..template import Transform2D
from .texture import Texture
# prefabricated
from .prefab.image import AsciiImage as Image
from .prefab.label import AsciiLabel as Label
from .prefab.line import AsciiLine as Line
from .prefab.sprite import AsciiSprite as Sprite
# networking
from . import networking


# -- activate ANSI escape codes
import os as _os
_os.system("")
# _os.system("cls") # used when developing
del _os
