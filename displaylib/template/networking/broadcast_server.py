from __future__ import annotations

import json
import socket

from .server import Server


class BroadcastServer(Server):
    """`BroadcastServer` that only broadcasts info to the other clients

    Data hooks (a raw request is split and deligated):
        - `system` : `_on_system_request(self, request: dict[str, str]) -> None`
        - `custom` : `_on_custom_request(self, request: dict[str, str]) -> None`
    """
    def __init__(self, *, host: str = "localhost", port: int = 8080, backlog: int = 4, **config) -> None:
        # self.connections: list[socket.socket] = [] # FIXME: client connection causes immediate error
        super().__init__(host=host, port=port, backlog=backlog, **config)
    
    def _on_client_connected(self, connection: socket.socket, _host: str, _port: int) -> None:
        # self.connections.append(connection)
        print(f"[Info] Disconnected {connection}")
    
    def _on_client_disconnected(self, connection: socket.socket, error: Exception) -> None:
        # self.connections.remove(connection) # FIXME: connection not in list. _on_client_connected not called
        print(f"[Info] Disconnected {connection}")
        print(f"[Cause] {error}")

    def _on_request_received(self, sender: socket.socket, request: bytes) -> None:
        """Distributes the byte request as a dict for each category

        Categories:
            - `system` : `_on_system_request(self, request: dict[str, str]) -> None`
            - `custom` : `_on_custom_request(self, request: dict[str, str]) -> None`

        Args:
            request (bytes): raw byte request in json with elements string serialized
        """
        # FIXME: add delimiter between JSON requests
        # FIXME: add buffer for request, else a request that is too long may crash the json.JSONDecoder
        data: dict[str, dict[str, dict[str, str]]] = json.loads(request.decode(self.encoding))
        # -- distribute request categories
        system = data["system"]
        self._on_system_request(system)
        custom = data["custom"]
        self._on_custom_request(custom)
        # -- broadcast data
        data_to_send: dict[str, dict[str, dict[str, str]]] = {"system": data["system"]} | {"custom": data["custom"]}
        as_json = json.dumps(data_to_send)
        encoded = bytes(as_json, self.encoding)
        for connection in tuple(self.connections):
            if connection == sender: # do not send to sender
                continue
            try:
                connection.sendall(encoded)
            except (ConnectionAbortedError, ConnectionResetError):
                self.connections.remove(connection)
                continue
