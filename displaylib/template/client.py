from __future__ import annotations

import socket
import selectors
import json

from ..template import Node


class SerializeError(TypeError): ...


def serialize(instance: object) -> str:
    """Calls the underlaying `__serialize__` on argument `instance`
    
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
    elif hasattr(instance, "__recipe__"): # important attributes to recreate an instance
        arg_values = []
        kwarg_values = []
        modification_values = []
        for instruction in instance.__recipe__:
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
    request_delimiter: str = "$"
    argument_delimiter: str = ":"
    encoding: str = "utf-8"
    _queued_changes: dict[str, dict[str, str]] = {}

    def __new__(cls: type[Client], *args, **kwargs) -> Client:
        instance = super().__new__(cls)

        def __setattr__(self, name: str, value: object):
            change = {name: serialize(value)}
            request = change
            local_uid = hex(id(self))
            if not local_uid in Client._queued_changes:
                Client._queued_changes[local_uid] = request
            else:
                Client._queued_changes[local_uid].update(request)
            return object.__setattr__(self, name, value)
        
        Node.__setattr__ = __setattr__
        for node in Node.nodes.values():
            node.__setattr__ = __setattr__
        return instance
        #request = bytes(json.dumps(change), cls.encoding)

    # TODO: build custom __init__ args
    def __init__(self, host: str, port: int) -> None:
        self._address = (host, port)
        self._sel = selectors.DefaultSelector()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sel.register(self._socket, selectors.EVENT_READ)
        self._socket.connect(self._address)
        self._socket.setblocking(False)
        self._buffer = bytes()

    def _on_request(self, data: str) -> None:
        ...
    
    def _update_socket(self) -> None:
        # -- send request
        if Client._queued_changes:
            request = bytes(json.dumps(Client._queued_changes), Client.encoding)
            Client._queued_changes.clear()
            if request:
                self.send_raw(request)
        # -- recieve request
        for key, mask in self._sel.select(timeout=self.timeout):
            connection = key.fileobj
            if mask & selectors.EVENT_READ:
                data = connection.recv(self.buffer_size)
                if data: # a readable client socket that has data.
                    if self.request_delimiter in data:
                        head, *rest = data.split(self.request_delimiter)
                        self._buffer += head
                        data = self._buffer.decode()
                        request, *args = data.split(self.argument_delimiter)
                        self._buffer = bytes()
                        self._on_request(request, list(args))
                        for content in rest[:-1]:
                            data = content.decode()
                            request, *args = data.split(self.argument_delimiter)
                            self._on_request(request, list(args))
                        self._buffer += rest[-1]
                    else:
                        self._buffer += data
                    # print('  received {!r}'.format(data))

    def send(self, request: str) -> None:
        encoded = request.encode(encoding="utf-8") + bytes(self.request_delimiter, "utf-8")
        self._socket.send(encoded)
    
    def send_raw(self, request: bytes) -> None:
        self._socket.send(request)
