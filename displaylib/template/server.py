from __future__ import annotations

import selectors
import socket


class Server:
    buffer_size: int = 4096
    timeout: float = 0
    encoding: str = "utf-8"

    def __init__(self, host: str = "localhost", port: int = 8080) -> None:
        self._address = (host, port)
        self._selector = selectors.DefaultSelector()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._selector.register(self._socket, selectors.EVENT_READ)
        self._buffer = bytes()
        try:
            self._socket.connect(self._address)
        except ConnectionRefusedError as error:
            self._on_connection_refused(error)
        self._on_connection_established
        self._socket.setblocking(False)

    def _on_connection_refused(self, error: Exception) -> None:
        ...

    def _on_connection_established(self, host: str, port: int) -> None:
        ...
