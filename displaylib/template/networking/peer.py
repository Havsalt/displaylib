from __future__ import annotations

import time
import socket
import selectors

from ..type_hints import MroNext, EngineType
from .structs import Request, Response


class Peer:
    PING_REQUEST: str = "PING_REQUEST"
    PING_REQUEST_ATTEMPTS: int = 32
    PING_REQUEST_DELTA: float = 0.01
    PING_RESPONSE: str = "PING_RESPONSE"
    buffer_size: int = 4096
    request_delimiter: str = "$"
    argument_delimiter: str = ";"
    encoding: str = "utf-8"
    backlog: int = 5
    timeout: float = 0
    request_batch: int = 32
    response_batch: int = 32
    _queued_requests: list[bytes] = []
    _queued_responses: list[bytes] = []
    _local_address: tuple[str, int]
    _peer_address: tuple[str, int]
    _selector: selectors.DefaultSelector
    _socket: socket.socket
    _buffer: bytes

    def __new__(cls: type[EngineType], *args, host: str = "localhost", port: int = 8080, peer_host: str = "localhost", peer_port: int = 7979, **kwargs) -> EngineType:
        mro_next = super() # type: MroNext[Peer] # type: ignore
        instance = mro_next.__new__(cls, *args, **kwargs)
        instance._local_address = (host, port)
        instance._peer_address = (peer_host, peer_port)
        instance._selector = selectors.DefaultSelector()
        instance._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        instance._selector.register(instance._socket, selectors.EVENT_READ)
        instance._buffer = bytes()
        instance._socket.setblocking(False)
        instance._socket.bind(instance._local_address)
        instance.per_frame_tasks.append(instance._update_socket) # type: ignore  # Engine task
        return instance # type: ignore
    
    def send(self, request: Request) -> None:
        """Sends a custom request

        Args:
            request (dict[Any, Any]): request to send
        """
        data = (request.kind + self.argument_delimiter + self.argument_delimiter.join(map(str, request.data)) + self.request_delimiter).encode(self.encoding)
        Peer._queued_requests.append(data)
    
    def is_peer_responsive(self) -> bool:
        data = (self.argument_delimiter.join(
            (
                self.PING_REQUEST,
                self._local_address[0],
                str(self._local_address[1])
            )
            ) + self.request_delimiter
            ).encode(self.encoding)
        for attempt in range(self.PING_REQUEST_ATTEMPTS):
            try:
                self._socket.sendto(data, self._peer_address)
            except OSError:
                return False
            try:
                raw_data, _address = self._socket.recvfrom(64)
                if raw_data.startswith(self.PING_RESPONSE.encode(self.encoding)):
                    return True
            except (BlockingIOError, ConnectionResetError):
                continue
            finally:
                if attempt != (self.PING_REQUEST_ATTEMPTS -1):
                    time.sleep(self.PING_REQUEST_DELTA)
        return False

    def _update_socket(self) -> None:
        """Updates the socket's I/O and calls `_on_request` with gathered Request object
        """
        # send requests
        batch = Peer._queued_requests[:self.request_batch]
        Peer._queued_requests = Peer._queued_requests[self.request_batch:]
        try:
            for data in batch:
                self._socket.sendto(data, self._peer_address) # send the request
        except OSError:
            return
        # recieve responses
        # TODO: implement batch request
        for _iteration in range(self.response_batch):
            for _key, mask in self._selector.select(timeout=self.timeout):
                if mask & selectors.EVENT_READ:
                    try:
                        response_bytes, _address = self._socket.recvfrom(self.buffer_size)
                    except OSError:
                        continue
                    parts = response_bytes.split(self.request_delimiter.encode(encoding=self.encoding))
                    response_string = parts[0].decode(self.encoding) # QUICKFIX: implement 'self._buffer'
                    kind, *data = response_string.split(self.argument_delimiter)
                    response = Response(kind=kind, data=data)
                    if kind == self.PING_REQUEST:
                        back_ping = (self.PING_RESPONSE + self.request_delimiter).encode(self.encoding)
                        self._socket.sendto(back_ping, self._peer_address)
                    else:
                        self._on_response(response)
    
    def _on_response(self, response: Response) -> None:
        ...
