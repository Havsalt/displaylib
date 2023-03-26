from __future__ import annotations

import json
import selectors
import socket
from typing import Any

from ..template import Node


class SerializeError(TypeError): ...


def serialize(instance: object) -> str:
    """Calls the underlaying `__serialize__` on argument `instance`.
    If not found, tries to serialize based on `__recipe__`
    
    ----
    #### Syntax of `__recipe__`:
        * `"[attr]"`  positional argument
        * `"[attr]="` keyword argument
        * `"[attr]!"` attribute is set after instance creation

    Args:
        instance (SupportsSerialize): instance to serialize

    Returns:
        str: serialized string
    """
    if hasattr(instance, "__serialize__"):
        return instance.__serialize__()
    
    elif instance.__class__.__module__ == "builtins":
        return str(instance)
    
    # alternative to implementing `__serialize__` (using `__recipe__`)
    elif hasattr(instance, "__recipe__"): # uses important attributes to recreate an instance
        arg_values = []
        kwarg_values = []
        modification_values = []
        for instruction in getattr(instance, "__recipe__"):
            attr, suffix, = instruction, ""
            if "!" in instruction:
                attr, suffix, _ = instruction.partition("!")
            else:
                attr, suffix, _ = instruction.partition("=")
            # do stuff
            if suffix == "!":
                value = attr + suffix + str(getattr(instance, attr))
                modification_values.append(value)
            elif suffix == "=":
                value = attr + suffix + str(getattr(instance, attr))
                kwarg_values.append(value)
            else:
                value = str(getattr(instance, attr))
                arg_values.append(value)
        values = (*arg_values, *kwarg_values, *modification_values)
        return f"{instance.__class__.__qualname__}({', '.join(values)})"
    raise SerializeError(f"instance of class '{instance.__class__.__qualname__}' missing either __serialized__ or __recipe__, or is not a builtin type")


class Client:
    buffer_size: int = 4096
    timeout: float = 0
    encoding: str = "utf-8"
    _queued_changes: dict[str, dict[str, dict[str, str]]] = {"system": {},"custom": {}}

    def __new__(cls: type[Client], *args, **kwargs) -> Client: # Engine instance
        def __setattr__(self: Node, name: str, value: object):
            """Overridden `__setattr__` that automaticlly queues changes to be sent as a network request
            """
            change = {name: serialize(value)}
            if self.uid not in Client._queued_changes["system"]:
                Client._queued_changes["system"][self.uid] = change
            else:
                Client._queued_changes["system"][self.uid].update(change)
            return object.__setattr__(self, name, value)

        Node.__setattr__ = __setattr__ # no nodes are made prior to this change
        instance = super().__new__(cls)
        return instance

    def __init__(self, host: str = "localhost", port: int = 8080, *args, **kwargs) -> None:
        self._address = (host, port)
        self._selector = selectors.DefaultSelector()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._selector.register(self._socket, selectors.EVENT_READ)
        self._buffer = bytes()
        try:
            self._socket.connect(self._address)
        except ConnectionRefusedError as error:
            self._on_connection_refused(error)
        self._on_connection_established(host, port)
        self._socket.setblocking(False)
        super(__class__, self).__init__(*args, **kwargs)
        self._update_socket()
    
    def _on_connection_refused(self, error: Exception) -> None:
        ...
    
    def _on_connection_established(self, host: str, port: int) -> None:
        ...

    def _on_response(self, response: str) -> None:
        ...
    
    def _update_socket(self) -> None:
        # -- send request
        if Client._queued_changes["system"] or Client._queued_changes["custom"]:
            request = bytes(json.dumps(Client._queued_changes), Client.encoding)
            Client._queued_changes = {"system": {},"custom": {}} # reset dict
            if request:
                self._socket.send(request) # send the request
        # -- recieve request
        for key, mask in self._selector.select(timeout=self.timeout):
            connection = key.fileobj
            if mask & selectors.EVENT_READ:
                data = connection.recv(self.buffer_size)
                if data: # indicates a readable client socket that has data
                    if self.request_delimiter in data:
                        head, *rest = data.split(self.request_delimiter)
                        self._buffer += head
                        data = self._buffer.decode()
                        response, *args = data.split(self.argument_delimiter)
                        self._buffer = bytes()
                        self._on_response(response, list(args))
                        for content in rest[:-1]:
                            data = content.decode()
                            response, *args = data.split(self.argument_delimiter)
                            self._on_response(response, list(args))
                        self._buffer += rest[-1]
                    else:
                        self._buffer += data
    
    def _main_loop(self) -> None:
        def sort_fn(element: tuple[int, Node]):
            return element[1].z_index
        
        delta = 1.0 / self.tps
        nodes = tuple(Node.nodes.values())
        while self.is_running:
            self._update(delta)
            for node in nodes:
                node._update(delta)

            for node in Node._queued_nodes:
                del Node.nodes[id(node)]
            Node._queued_nodes.clear()

            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            nodes = tuple(Node.nodes.values())

            self._update_socket()

    def send(self, request: dict[str, dict[str, Any]]) -> None:
        """Queues the request to be sent

        Format: `{node_id: {attr, value}, ...}`. Treated as "custom" when sent to server (instead of "system")

        Args:
            request (dict[int, dict[str, Any]]): the changes to be sent
        """
        # -- serialize each change
        for uid, changes in request.items():
            for name, value in changes.items():
                change = {name: serialize(value)}
                if uid not in Client._queued_changes["custom"]:
                    Client._queued_changes["custom"][uid] = change
                else:
                    Client._queued_changes["custom"][uid].update(change)
