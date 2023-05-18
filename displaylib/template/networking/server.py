from __future__ import annotations

import selectors
import socket


class Server:
    """`Server` base class

    Hooks:
        - `_on_connection_refused(self, error: Exception) -> None`
        - `_on_client_connected(self, connection: socket.socket, host: str, port: int) -> None`
        - `_on_client_disconnected(self, connection: socket.socket, error: Exception) -> None`
        - `_on_request_received(self, sender: socket.socket, request: bytes) -> None`
        - `_on_system_request(self, request: dict[str, str]) -> None`
        - `_on_custom_request(self, request: dict[str, str]) -> None`
    """
    buffer_size: int = 4096
    timeout: float = 0
    encoding: str = "utf-8"

    def __init__(self, *, host: str = "localhost", port: int = 8080, backlog: int = 4, **config) -> None:
        """Initializes `Server` functionality on the `Engine`

        Args:
            host (str, optional): host name. Defaults to "localhost".
            port (int, optional): port number. Defaults to 8080.
            backlog (int, optional): number of connections allowed to connect at once. Defaults to 4.
        """
        self._address = (host, port)
        self._selector = selectors.DefaultSelector()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._selector.register(self._socket, selectors.EVENT_READ)
        # self._buffer = bytes()
        try:
            self._socket.bind(self._address)
            self._socket.listen(backlog)
        except ConnectionRefusedError as error:
            self._on_connection_refused(error)
            return # does not start the main loop if failed to connect
        self._socket.setblocking(False)
        self.per_frame_tasks.append(self._update_socket) # Engine task
        super(__class__, self).__init__(**config)

    def _on_connection_refused(self, error: Exception) -> None:
        """Override for custom functionality

        Args:
            error (Exception): reason server socket did not start
        """
        ...

    def _on_client_connected(self, connection: socket.socket, host: str, port: int) -> None:
        """Override for custom functionality

        Args:
            connection (socket.socket): the newly established connection
            host (str): host name
            port (int): port number
        """
        ...
    
    def _on_client_disconnected(self, connection: socket.socket, error: Exception) -> None:
        """Override for custom functionality

        Args:
            connection (socket.socket): connection that was lost
            error (Exception): error that occured
        """
        ...

    def _on_request_received(self, sender: socket.socket, request: bytes) -> None:
        """Override for custom functionality
        
        Args:
            request (bytes): byte encoded json request recieved
        """
        ...
    
    def _on_system_request(self, request: dict[str, dict[str, str]]) -> None:
        """Override for custom functionality

        Args:
            request (dict[str, dict[str, str]]): dict with string encoded changes for catagory `system`
        """
        ...
    
    def _on_custom_request(self, request: dict[str, dict[str, str]]) -> None:
        """Override for custom functionality

        Args:
            request (dict[str, dict[str, str]]): dict with string encoded changes for catagory `custom`
        """
        ...
    
    def _update_socket(self) -> None:
        """Updates the socket's I/O and calls `_on_request_received` with the bytes received as argument
        """
        # -- recieve request
        for key, mask in self._selector.select(timeout=self.timeout):
            connection = key.fileobj
            if mask & selectors.EVENT_READ:
                try:
                    request: bytes = connection.recv(self.buffer_size)
                except OSError as error:
                    self._selector.unregister(connection)
                    self._on_client_disconnected(connection, error)
                    continue
                if request:
                    self._on_request_received(connection, request)
        # -- accept connection if one is incoming
        try:
            connection, (host, port) = self._socket.accept()
            self._selector.register(connection, selectors.EVENT_READ)
            self._on_client_connected(connection, host, port)
        except BlockingIOError:
            return
