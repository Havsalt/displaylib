"""## Ascii submodule of DisplayLib

Provides a framework for creating infinite 2D worlds in Ascii
"""

__all__ = [
    # math
    "lerp",              # (function)
    "sign",              # (function)
    "Vec2",              # (data structure)
    "Vec2i",             # (data structure)
    # utility
    "autorun",           # (class decorator)
    "debug",             # (function)
    "load_texture",      # (function)
    # base
    "BaseNode",          # (class alias)
    # core ascii
    "Node",              # (class)
    "Node2D",            # (class)
    "Engine",            # (class)
    "Camera",            # (class)
    "Screen",            # (class)
    "AnimationFrame",    # (class)
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
    "text",              # (module)
    # networking
    "networking",        # (module)
    # typing support
    "AnyNode",           # (protocol)
    "ColorValue"         # (type alias)
]

# math
from ..math import lerp, sign, Vec2, Vec2i
# utility
from ..util import autorun
from .debug import debug
from .texture import load_texture
# base
from ..template import Node as BaseNode
# core ascii
from .node import AsciiNode as Node, AsciiNode2D as Node2D
from .engine import AsciiEngine as Engine
from .camera import AsciiCamera as Camera
from .screen import AsciiScreen as Screen
from .animation import AnimationFrame, Animation, EmptyAnimation, AnimationPlayer
from .audio import AudioStreamPlayer
from .clock import Clock
# mixin components
from ..template import Transform2D
from .texture import Texture
from .colored import Color
# prefabricated
from .prefabs.label import AsciiLabel as Label
from .prefabs.line import AsciiLine as Line
from .prefabs.sprite import AsciiSprite as Sprite
# generating colors
from . import color
# text alteration
from . import text
# networking
from ..template import networking
# typing support
from ..template.type_hints import AnyNode
from .color import ColorValue


# activate ANSI escape codes
import os as _os
_os.system("")
del _os
