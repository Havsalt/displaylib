from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ...template.type_hints import MroNext, NodeType, AnyNode
from ..node import AsciiNode2D
from ..texture import Texture
from ..colored import Color
from ..color import WHITE

if TYPE_CHECKING:
    from ...template.type_hints import AnyNode
    from ..color import ColorValue


class Panel(Color, Texture, AsciiNode2D):
    width: int = 12
    height: int = 16
    
    def __new__(cls: type[NodeType], *args, width: int = 12, height: int = 8, **kwargs) -> NodeType:
        mro_next = cast(MroNext[Panel], super())
        instance = mro_next.__new__(cls, *args, **kwargs)
        # property updaters
        instance._width = width
        instance._height = height
        instance.texture = [
            ["+", *("-"*(width-2)), "+"],
            *(["|", *(" "*(width-2)), "|"] for _ in range(height-2)),
            ["+", *("-"*(width-2)), "+"]
        ]
        return cast(NodeType, instance)
    
    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, width: int = 12, height: int = 8, color: ColorValue = WHITE, centered: bool = False, z_index: int = 0, force_sort: bool = True) -> None:
        ...
    
    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value
        self.texture = [
            ["+", *("-"*(value-2)), "+"],
            *(["|", *(" "*(value-2)), "|"] for _ in range(self._height-2)),
            ["+", *("-"*(value-2)), "+"]
        ]
    
    @property
    def height(self) -> int:
        return self._height

    @width.setter
    def height(self, value: int) -> None:
        self._height = value
        self.texture = [
            ["+", *("-"*(self._width-2)), "+"],
            *(["|", *(" "*(self._width-2)), "|"] for _ in range(value-2)),
            ["+", *("-"*(self._width-2)), "+"]
        ]
