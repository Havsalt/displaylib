from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ...math import Vec2i
from ...template.type_hints import MroNext, NodeType, AnyNode
from ..node import AsciiNode2D
from ..texture import Texture
from ..colored import Color
from ..color import WHITE

if TYPE_CHECKING:
    from ...template.type_hints import AnyNode
    from ..color import ColorValue


class PanelStyle:
    # top
    top_left:   str = "+"
    top_middle: str = "-"
    top_right:  str = "+"
    # middle
    middle_left:  str = "|"
    middle_fill:  str = " "
    middle_right: str = "|"
    # bottom
    bottom_left:   str = "+"
    bottom_middle: str = "-"
    bottom_right:  str = "+"


class Panel(Color, Texture, AsciiNode2D):
    default_width: int
    default_height: int
    style: PanelStyle
    
    def __new__(cls: type[NodeType], *args, width=None, height=None, style=None, **kwargs) -> NodeType:
        mro_next = cast(MroNext[Panel], super())
        instance = mro_next.__new__(cls, *args, **kwargs)
        # set width
        if width is not None:
            instance._width = width
        elif hasattr(instance, "default_width"):
            instance._width = instance.default_width
        else:
            instance._width = 12
        # set height
        if height is not None:
            instance._height = height
        elif hasattr(instance, "default_height"):
            instance._height = instance.default_height
        else:
            instance._height = 12
        # set style
        if style is not None:
            instance.style = style
        elif hasattr(instance, "style"):
            instance.style = instance.style
        else:
            instance.style = PanelStyle()
        # update texture
        instance.texture = [
            [instance.style.top_left, *(instance.style.top_middle*(instance._width-2)), instance.style.top_right],
            *([instance.style.middle_left, *(instance.style.middle_fill*(instance._width-2)), instance.style.middle_right] for _ in range(instance._height-2)),
            [instance.style.bottom_left, *(instance.style.bottom_middle*(instance._width-2)), instance.style.bottom_right]
        ]
        return cast(NodeType, instance)
    
    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, width: int = 12, height: int = 8, color: ColorValue = WHITE, centered: bool = False, style: PanelStyle | None = None, z_index: int = 0, force_sort: bool = True) -> None:
        """Panel interface

        Args:
            parent (AnyNode | None, optional): parent node. Defaults to None.
            x (float, optional): local x position. Defaults to 0.
            y (float, optional): local y position. Defaults to 0.
            width (int, optional): width override. Defaults to 12.
            height (int, optional): height override. Defaults to 8.
            color (ColorValue, optional): applied color. Defaults to WHITE.
            centered (bool, optional): whether to center the panel around its origin. Defaults to False.
            z_index (int, optional): layer priority. Defaults to 0.
            force_sort (bool, optional): whether to request force sort. Defaults to True.
        """
    
    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value
        self.texture = [
            [self.style.top_left, *(self.style.top_middle*(self._width-2)), self.style.top_right],
            *([self.style.middle_left, *(self.style.middle_fill*(self._width-2)), self.style.middle_right] for _ in range(self._height-2)),
            [self.style.bottom_left, *(self.style.bottom_middle*(self._width-2)), self.style.bottom_right]
        ]
    
    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value
        self.texture = [
            [self.style.top_left, *(self.style.top_middle*(self._width-2)), self.style.top_right],
            *([self.style.middle_left, *(self.style.middle_fill*(self._width-2)), self.style.middle_right] for _ in range(self._height-2)),
            [self.style.bottom_left, *(self.style.bottom_middle*(self._width-2)), self.style.bottom_right]
        ]
    
    def size(self) -> Vec2i:
        return Vec2i(self._width, self._height)
