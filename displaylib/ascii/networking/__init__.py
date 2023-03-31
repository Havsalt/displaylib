"""## Networking submodule of DisplayLib.ascii

Provies both `Client` and `Server` classes for integrating networking compatible with `displaylib.ascii`
"""

__all__ = [
    "serialize",
    "deserialize",
    "SerializeError",
    "Client",
    "Server",
    "BroadcastServer"
]

from ...template.networking import serialize, deserialize, SerializeError
from .client import ASCIIClient as Client
from .server import ASCIIServer as Server
from .broadcast_server import ASCIIBroadcastServer as BroadcastServer
