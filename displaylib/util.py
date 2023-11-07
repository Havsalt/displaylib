from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING, Callable as _Callable, Any as _Any
from functools import wraps as _wraps

if _TYPE_CHECKING:
    from .template.type_hints import P as _P, R as _R, Engine as _Engine

__all__ = [
    "autorun",
    # "extend"
]

def autorun(**config: _Any) -> ...:
    def run(app: _Callable[..., _Engine]) -> None:
        app(**config) # runs the app
    return run

# FIXME: implement
# def extend(method: _Callable[_P, _R]) -> _Callable[_P, _R]:
#     return method # NOTE: quickfix, disabled
#     @_wraps(method)
#     def function(*args: _P.args, **kwargs: _P.kwargs) -> _R:
#         self, *arguments = args
#         mro = type(self).__mro__
#         for base in mro:
#             if hasattr(base, method.__name__):
#                 ...
#         else: # nobreak
#             raise AttributeError("did not find method " + method.__name__) # TODO: make prettier
#         return method(self, *arguments, **kwargs) # type: ignore
#     return function # type: ignore
