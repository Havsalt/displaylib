from __future__ import annotations as _annotations

import weakref as _weakref
import time as _time
import re as _re
import inspect as _inspect
from types import FrameType as _FrameType
from typing import TypeVar as _TypeVar, Protocol as _Protocol, Generic as _Generic, Optional as _Optional

from ..template import BaseNode as _BaseNode
from .camera import AsciiCamera as _AsciiCamera
from .prefabs.label import AsciiLabel as _AsciiLabel

_T = _TypeVar("_T", covariant=True)

class _WeakRef(_Generic[_T], _Protocol):
    def __call__(self) -> _Optional[_T]: ...


class _DebugInfo:
    def __init__(self, ref: _WeakRef[_AsciiLabel], *, lifetime: float = 10.0) -> None:
        self.ref = ref
        self.lifetime = lifetime
        self.life_start = _time.time()


_PATTERN = _re.compile(r"debug\((.*)\)")
_debug_info: dict[str, _DebugInfo] = {}


def debug(*objects: object, escape: bool = False, label: str | None = None, lifetime: float = 10.0, sep: str = " ") -> None:
    global _debug_info
    text = sep.join(map(str, objects))
    if label is None:
        frame = _inspect.currentframe().f_back # type: _FrameType  # type: ignore
        frame_info = _inspect.getframeinfo(frame) # type: _inspect.FrameInfo  # type: ignore
        line = frame_info.code_context[0] # type: str  # type: ignore
        name = _PATTERN.findall(line)[0] # first match
    else:
        name = label
    # modify if exists
    for key, info in _debug_info.items():
        if (alive_node := info.ref()) is not None:
            if (kinda_alive_node := alive_node) not in _BaseNode.nodes.values():
                if kinda_alive_node in _debug_info.keys():
                    del _debug_info[key]
                    continue
            if key == name:
                alive_node.text = (text if not escape else repr(text))
                info.lifetime = lifetime # give new life
                info.life_start = _time.time()
                break
        else: # cleanup known unused (ref not valid)
            del _debug_info[key]
    else: # no break
        # store new weak ref
        node = _AsciiLabel(text=(text if not escape else repr(text)))
        if _debug_info:
            info = _DebugInfo(_weakref.ref(node), lifetime=lifetime)
        else:
            info = _DebugInfo(_weakref.ref(node), lifetime=lifetime)
        _debug_info[name] = info
    # order output
    fn = lambda elements: elements[1].life_start
    _debug_info = {k: v for k, v in sorted(_debug_info.items(), key=fn, reverse=True)}
    y = 0
    # TODO: calc pos each time
    origin = _AsciiCamera.current.get_global_position()
    for key, info in tuple(_debug_info.items()):
        if (node := info.ref()) is not None:
            # calculate lifetime
            time_elapsed = _time.time() - info.life_start
            if time_elapsed >= info.lifetime:
                node.queue_free()
                del _debug_info[key]
                continue
            node.position = origin.copy()
            node.position.y += y
            y += 1
