from __future__ import annotations

import selectors
import socket
from typing import ClassVar

from ..type_hints import EngineType
from .structs import Request, Response


class Server:
    """`Server` mixin class

    Hooks:
        - `_on_connection_refused(self, error: Exception) -> None`
        - `_on_client_connected(self, connection: socket.socket, host: str, port: int) -> None`
        - `_on_client_disconnected(self, connection: socket.socket, error: Exception) -> None`
        - `_on_response(self, sender: socket.socket, response: Response) -> None`
    """
    buffer_size: int = 4096
    request_delimiter: str = "$"
    argument_delimiter: str = ";"
    encoding: str = "utf-8"
    backlog: int = 5
    timeout: float = 0
    request_batch: int = 32
    response_batch: int = 32
    _queued_requests: ClassVar[list[tuple[socket.socket, bytes]]] = []
    _queued_responses: ClassVar[list[tuple[socket.socket, bytes]]] = []
    _address: tuple[str, int]
    _selector: selectors.DefaultSelector
    _socket: socket.socket

    def __new__(cls: type[EngineType], *, host: str = "localhost", port: int = 8080, backlog: int = 4, **config) -> EngineType:
        """Adds `Server` functionality on the `Engine`

        Added Args:
            host (str, optional): host name. Defaults to "localhost".
            port (int, optional): port number. Defaults to 8080.
            backlog (int, optional): number of connections allowed to connect at once. Defaults to 4.
        """
        instance = super().__new__(cls, **config) # type: Server  # type: ignore
        # class value -> override -> default
        final_host = getattr(instance, "host", host)
        # class value -> override -> default
        final_port = getattr(instance, "port", port)
        instance._address = (final_host, final_port)
        instance._selector = selectors.DefaultSelector()
        instance._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        instance._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        instance._selector.register(instance._socket, selectors.EVENT_READ)
        try:
            instance._socket.bind(instance._address)
            instance._socket.listen(backlog)
        except ConnectionRefusedError as error:
            instance._on_connection_refused(error)
            return instance # type: ignore  # does not start the main loop if failed to connect
        instance._socket.setblocking(False)
        instance.per_frame_tasks.append(instance._update_socket) # type: ignore  # Engine task
        return instance # type: ignore
    
    @property
    def connections(self) -> list[socket.socket]:
        return [key.fileobj # type: ignore
                for key in self._selector.get_map().values()]

    def send_to(self, request: Request, /, connection: socket.socket) -> None:
        data = (request.kind + self.argument_delimiter + self.argument_delimiter.join(map(str, request.data)) + self.request_delimiter).encode(self.encoding)
        data_pair = (connection, data)
        Server._queued_requests.append(data_pair)
    
    def broadcast(self, request: Request, /) -> None:
        data = (request.kind + self.argument_delimiter + self.argument_delimiter.join(map(str, request.data)) + self.request_delimiter).encode(self.encoding)
        for connection in self.connections:
            data_pair = (connection, data) # type: tuple[socket.socket, bytes]  # type: ignore
            Server._queued_requests.append(data_pair)

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

    def _on_response(self, connection: socket.socket, response: Response) -> None:
        """Override for custom functionality

        Args:
            connection (socket.socket): connection the response was sent from
            response (Response): response received
        """
        ...
    
    def _update_socket(self) -> None:
        """Updates the socket's I/O and calls `_on_request` with the bytes received as argument
        """
        # send requests
        batch = Server._queued_requests[:self.request_batch]
        Server._queued_requests = Server._queued_requests[self.request_batch:]
        # try:
        for connection, data in batch:
            print(connection, data)
            connection.send(data)
        # except OSError:
        #     pass
        # recieve responses
        try:
            for key, mask in self._selector.select(timeout=self.timeout):
                connection = key.fileobj # type: socket.socket  # type: ignore
                if mask & selectors.EVENT_READ:
                    for _iteration in range(self.response_batch):
                        try:
                            response_bytes = connection.recv(self.buffer_size)
                            if not response_bytes:
                                reason = ConnectionAbortedError("Client is not responding")
                                # self._selector.unregister(connection) # FIXME
                                self._on_client_disconnected(connection, reason)
                                continue
                        except OSError as error:
                            # self._selector.unregister(connection) # FIXME
                            self._on_client_disconnected(connection, error)
                            continue
                        parts = response_bytes.split(self.request_delimiter.encode(encoding=self.encoding))
                        response_string = parts[0].decode(self.encoding)
                        kind, *data = response_string.split(self.argument_delimiter)
                        response = Response(kind=kind, data=data)
                        self._on_response(connection, response)
        except OSError:
            pass
        # accept connection if one is incoming
        try:
            connection, (host, port) = self._socket.accept()
            self._selector.register(connection, selectors.EVENT_READ)
            self._on_client_connected(connection, host, port)
        except BlockingIOError:
            pass
