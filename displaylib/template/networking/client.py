from __future__ import annotations

import uuid
import json
import selectors
import socket
from typing import TypeVar, Any

from ...template import Node
from .serialize import serialize

EngineLike = TypeVar("EngineLike")


class Client:
    """`Client` base class

    Hooks:
        - `_on_connection_refused(self, error: Exception) -> None`
        - `_on_connection_established(self, host: str, port: int) -> None`
        - `_on_response_received(self, response: bytes) -> None`
        - `_on_response(self, response: str) -> None`
    """
    buffer_size: int = 4096 * 16
    timeout: float = 0
    encoding: str = "utf-8"
    uids_buffer_size: int = 1_000
    _premade_uids: list[str] = [uuid.uuid1().hex for _ in range(uids_buffer_size)]
    _queued_changes: dict[str, dict[str, dict[str, str]]] = {"system": {},"custom": {}} # TODO: add 'pickle' category

    def __new__(cls: type[EngineLike], *args, **kwargs) -> EngineLike:
        # DISABLED: auto broadcast attribute changes
        # def __setattr__(self: Node, name: str, value: object) -> None:
        #     """Overridden `__setattr__` that automaticlly queues changes to be sent as a network request
        #     """
        #     change = {name: serialize(value)}
        #     object.__setattr__(self, name, value)
        #     if self.uid not in Client._queued_changes["system"]:
        #         Client._queued_changes["system"][self.uid] = change
        #     else:
        #         Client._queued_changes["system"][self.uid].update(change)
        # setattr(Node, "__setattr__", __setattr__)

        def __serialize__(self) -> str:
            """Low level implementation for serializing nodes

            Returns:
                str: serialized data about this node
            """
            return f"{self.__class__.__name__}()"
        setattr(Node, "__serialize__", __serialize__)

        @classmethod
        def generate_uid(_node_cls) -> str:
            """Generates a unique ID using uuid.uuid1().hex

            Returns:
                str: unique ID in the form of uuid.uuid1().hex
            """
            uid = cls._premade_uids[Node._uid_counter] # remember that `cls` in this function is from Client
            Node._uid_counter += 1
            if Node._uid_counter >= cls.uids_buffer_size:
                Node._uid_counter = 0
                cls._premade_uids = [uuid.uuid1().hex for _ in range(cls.uids_buffer_size)]
            return uid # globally unique (includes across networks)

        setattr(Node, "generate_uid", generate_uid) # updates the method

        instance = super().__new__(cls) # no nodes are made prior to these changes
        return instance

    def __init__(self, *, host: str = "localhost", port: int = 8080, **kwargs) -> None:
        """Initializes `Client` functionality on the `Engine`

        Args:
            host (str, optional): host name. Defaults to "localhost".
            port (int, optional): port number. Defaults to 8080.
        """
        self._address = (host, port)
        self._selector = selectors.DefaultSelector()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._selector.register(self._socket, selectors.EVENT_READ)
        # self._buffer = bytes()
        try:
            self._socket.connect(self._address)
        except ConnectionRefusedError as error:
            self._on_connection_refused(error)
        self._on_connection_established(host, port)
        self._socket.setblocking(False)
        self.per_frame_tasks.append(self._update_socket) # Engine task
        super(__class__, self).__init__(**kwargs)
    
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
    
    def _on_response_received(self, response: bytes) -> None:
        """Override for more controlled functionality

        Args:
            response (bytes): raw byte response in json with elements string serialized
        """
        self._on_response(response.decode(self.encoding))

    def _on_response(self, response: str) -> None:
        """Override for custom functionality

        Args:
            response (str): the processed response after `_on_response`
        """
        ...
    
    def _update_socket(self) -> None:
        """Updates the socket's I/O and calls `_on_response_received` with the bytes received as argument
        """
        # -- send request
        if Client._queued_changes["system"] or Client._queued_changes["custom"]:
            request = json.dumps(Client._queued_changes).encode(Client.encoding)
            Client._queued_changes = {"system": {},"custom": {}} # reset dict
            if request:
                self._socket.sendall(request) # send the request
        # -- recieve request
        for key, mask in self._selector.select(timeout=self.timeout):
            connection = key.fileobj
            if mask & selectors.EVENT_READ:
                try:
                    response: bytes = connection.recv(self.buffer_size)
                except (ConnectionAbortedError, ConnectionResetError) as error:
                    print(f"[!] Disconnected from server: {error}")
                    self._selector.unregister(connection)
                    self._socket.shutdown(socket.SHUT_RDWR)
                    self._socket.close()
                    return
                if response:
                    self._on_response_received(response)
    
    def send(self, request: dict[str, dict[str, Any]]) -> None:
        """Queues the request to be sent

        Format: `{node_id: {attr, value}, ...}`. Treated as "custom" when sent to server (instead of "system")

        Args:
            request (dict[str, dict[str, Any]]): the changes to be sent
        """
        # -- serialize each change
        for uid, changes in request.items():
            for name, value in changes.items():
                change = {name: serialize(value)}
                if uid not in Client._queued_changes["custom"]:
                    Client._queued_changes["custom"][uid] = change
                else:
                    Client._queued_changes["custom"][uid].update(change)
