from __future__ import annotations

from collections.abc import Iterable
from typing import NamedTuple, Any


class Request(NamedTuple):
    kind: str
    data: Iterable[Any] = []

    @staticmethod
    def from_response(response: Response, /) -> Request:
        return Request(**response._asdict())

    def to_response(self) -> Response:
        return Response(**self._asdict())


class Response(NamedTuple):
    kind: str
    data: Iterable[str] = []

    @staticmethod
    def from_request(request: Request, /) -> Response:
        return Response(**request._asdict())
    
    def to_request(self) -> Request:
        return Request(**self._asdict())
