"""ASCII submodule from DisplayLib
"""

__all__ = [
    "Vec2",
    "overload",
    "OverloadUnmatched",
    "Node",
    "Engine",
    "Camera",
    "Surface",
    "Client"
]

from ..math import Vec2
from ..overload import overload, OverloadUnmatched
from .node import ASCIINode as Node
from .engine import ASCIIEngine as Engine
from .camera import ASCIICamera as Camera
from .surface import ASCIISurface as Surface
from .client import ASCIIClient as Client

# activate ANSI escape codes
import os as _os
_os.system("")
_os.system("cls") # DEV
del _os
