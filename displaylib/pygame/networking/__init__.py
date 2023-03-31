"""## Networking submodule of DisplayLib.pygame

Provides both `Client` and `Server` classes for integrating networking compatible with `displaylib.pygame`
"""

__all__ = [
    "serialize",
    "deserialize",
    "SerializeError",
    "Client",
    "Server",
    "BroadcastServer"
]
# currently only using classes and functions from template
from ...template.networking import *
