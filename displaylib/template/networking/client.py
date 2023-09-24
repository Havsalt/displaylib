from __future__ import annotations

import socket
from typing import ClassVar

from ..type_hints import EngineType
from .structs import Request, Response


class Client:
    """`Client` base class

    Hooks:
        - `_on_connection_refused(self, error: Exception) -> None`
        - `_on_connection_established(self, host: str, port: int) -> None`
        - `_on_response_received(self, response: bytes) -> None`
        - `_on_response(self, response: str) -> None`
    """
    buffer_size: int = 4096
    request_delimiter: str = "$"
    argument_delimiter: str = ";"
    encoding: str = "utf-8"
    timeout: float = 0
    request_batch: int = 32
    response_batch: int = 32
    _queued_requests: ClassVar[list[bytes]] = []
    _queued_responses: ClassVar[list[bytes]] = []
    _address: tuple[str, int]
    _socket: socket.socket

    def __new__(cls: type[EngineType], *, host: str = "localhost", port: int = 8080, **config) -> EngineType:
        """Adds `Client` functionality on the `Engine`

        Added Args:
            host (str, optional): host name. Defaults to "localhost".
            port (int, optional): port number. Defaults to 8080.
            backlog (int, optional): number of connections allowed to connect at once. Defaults to 4.
        """
        instance = super().__new__(cls, **config) # type: Client  # type: ignore
        # class value -> class value -> default
        final_host = getattr(instance, "host", host)
        # class value -> override -> default
        final_port = getattr(instance, "port", port)
        instance._address = (final_host, final_port)
        instance._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        instance._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            instance._socket.connect(instance._address)
            instance._on_connection_established(final_host, final_port)
        except ConnectionRefusedError as error:
            instance._on_connection_refused(error)
            return instance # type: ignore  # does not start the main loop if failed to connect
        instance._socket.setblocking(False)
        instance.per_frame_tasks.append(instance._update_socket) # type: ignore  # Engine task
        return instance # type: ignore

    def send(self, request: Request) -> None:
        data = (request.kind + self.argument_delimiter + self.argument_delimiter.join(map(str, request.data)) + self.request_delimiter).encode(self.encoding)
        Client._queued_requests.append(data)
    
    def _on_connection_refused(self, error: Exception) -> None:
        """Override for custom functionality

        Args:
            error (Exception): error thrown when the connection was refused
        """
        ...
    
    def _on_connection_established(self, host: str, port: int) -> None:
        """Override for custom functionality

        Args:
            host (str): host name which the socket is connected to
            port (int): port number which the socket is connected to
        """
        ...
    
    def _on_response(self, response: Response) -> None:
        """Override for custom functionality

        Args:
            response (Response): response data
        """
        ...
    
    def _on_connection_ended(self, error: Exception) -> None:
        """Override for custom functionality

        Args:
            error (Exception): reason for the unexpected disconnection
        """
        raise ConnectionAbortedError("Server ended connection")

    def _update_socket(self) -> None:
        """Updates the socket's I/O and calls `_on_request` with gathered Request object
        """
        """Updates the socket's I/O and calls `_on_request` with the bytes received as argument
        """
        # send requests
        batch = Client._queued_requests[:self.request_batch]
        Client._queued_requests = Client._queued_requests[self.request_batch:]
        try:
            for data in batch:
                self._socket.send(data)
        except OSError:
            pass
        # recieve responses
        for _iteration in range(self.response_batch):
            try:
                response_bytes = self._socket.recv(self.buffer_size)
                if not response_bytes:
                    reason = ConnectionAbortedError("Server is not responding")
                    self._on_connection_ended(reason)
                    continue
            except (BlockingIOError, ConnectionResetError):
                continue
            parts = response_bytes.split(self.request_delimiter.encode(encoding=self.encoding))
            response_string = parts[0].decode(self.encoding)
            kind, *data = response_string.split(self.argument_delimiter)
            response = Response(kind=kind, data=data)
            self._on_response(response)

        # try:
        #     for _iteration in range(self.response_batch):
        #         try:
        #             response_bytes = self._socket.recv(self.buffer_size)
        #             if not response_bytes:
        #                 # reason = ConnectionAbortedError("Server is not responding")
        #                 # self._on_connection_ended(reason)
        #                 continue
        #         except OSError as error:
        #             self._on_connection_ended(error)
        #             continue
        #         parts = response_bytes.split(self.request_delimiter.encode(encoding=self.encoding))
        #         response_string = parts[0].decode(self.encoding)
        #         kind, *data = response_string.split(self.argument_delimiter)
        #         response = Response(kind=kind, data=data)
        #         self._on_response(response)
        # except OSError as error:
        #     self._on_connection_ended(error)
        #     self.is_running = False # type: ignore  # Engine attribute
        #     return
