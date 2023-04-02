"""## Networking submodule of DisplayLib.ascii

Provies both `Client` and `Server` classes for integrating networking compatible with `displaylib.ascii`
"""

__all__ = [
    "register_class",
    "serialize",
    "deserialize",
    "SerializeError",
    "DeserializeError",
    "Client",
    "Server",
    "BroadcastServer"
]

from ...template.networking import register_class, serialize, deserialize, SerializeError, DeserializeError
from .client import ASCIIClient as Client
from .server import ASCIIServer as Server
from .broadcast_server import ASCIIBroadcastServer as BroadcastServer
