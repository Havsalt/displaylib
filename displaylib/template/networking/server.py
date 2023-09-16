from __future__ import annotations

import selectors
import socket
from typing import TYPE_CHECKING, Protocol, cast

from ..type_hints import MroNext, EngineType, EngineMixin

if TYPE_CHECKING:
    from types import FunctionType

class ServerMixin(Protocol):
    @property
    def _address(self) -> tuple[str | int, int]: ...
    @_address.setter
    def _address(self, value: tuple[str | int, int]) -> None: ...
    @property
    def _selector(self) -> selectors.DefaultSelector: ...
    @_selector.setter
    def _selector(self, value: selectors.DefaultSelector) -> None: ...
    @property
    def _socket(self) -> socket.socket: ...
    @_socket.setter
    def _socket(self, value: socket.socket) -> None: ...
    @property
    def _buffer(self) -> bytes: ...
    @_buffer.setter
    def _buffer(self, value: bytes) -> None: ...
    @property
    def _update_socket(self) -> FunctionType: ...
    def _on_connection_refused(self, error: Exception) -> None: ...
    def _on_client_connected(self, connection: socket.socket, host: str, port: int) -> None: ...
    def _on_client_disconnected(self, connection: socket.socket, error: Exception) -> None: ...
    def _on_request_received(self, sender: socket.socket, request: bytes) -> None: ...
    def _on_system_request(self, request: dict[str, str]) -> None: ...
    def _on_custom_request(self, request: dict[str, str]) -> None: ...

class ValidServer(ServerMixin, EngineMixin, Protocol): ...


class Server:
    """`Server` mixin class

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
    _socket: socket.socket
    _address: tuple[str, int]
    _selector: selectors.DefaultSelector

    def __new__(cls: type[EngineType], *, host: str = "localhost", port: int = 8080, backlog: int = 4, **config) -> EngineType:
        """Adds `Server` functionality on the `Engine`

        Added Args:
            host (str, optional): host name. Defaults to "localhost".
            port (int, optional): port number. Defaults to 8080.
            backlog (int, optional): number of connections allowed to connect at once. Defaults to 4.
        """
        mro_next = cast(MroNext[ValidServer], super())
        instance = mro_next.__new__(cls, **config)
        # class value -> override -> default
        host = getattr(instance, "host", host)
        # class value -> override -> default
        port = getattr(instance, "port", port)
        instance._address = (host, port)
        instance._selector = selectors.DefaultSelector()
        instance._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        instance._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        instance._selector.register(instance._socket, selectors.EVENT_READ)
        instance._buffer = bytes()
        try:
            instance._socket.bind(instance._address)
            instance._socket.listen(backlog)
        except ConnectionRefusedError as error:
            instance._on_connection_refused(error)
            return cast(EngineType, instance) # does not start the main loop if failed to connect
        instance._socket.setblocking(False)
        instance.per_frame_tasks.append(instance._update_socket)
        return cast(EngineType, instance)

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
        # recieve request
        for key, mask in self._selector.select(timeout=self.timeout):
            connection = cast(socket.socket, key.fileobj)
            if mask & selectors.EVENT_READ:
                try:
                    request: bytes = connection.recv(self.buffer_size)
                except OSError as error:
                    self._selector.unregister(connection)
                    self._on_client_disconnected(connection, error)
                    continue
                if request:
                    self._on_request_received(connection, request)
        # accept connection if one is incoming
        try:
            connection, (host, port) = self._socket.accept()
            self._selector.register(connection, selectors.EVENT_READ)
            self._on_client_connected(connection, host, port)
        except BlockingIOError:
            return
