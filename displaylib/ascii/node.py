from __future__ import annotations

from typing import TYPE_CHECKING

from displaylib.template.type_hints import AnyNode

from ..template import Node, Transform2D

if TYPE_CHECKING:
    from ..math import Vec2i
    from .engine import AsciiEngine


class Ascii: # mode class with common hooks
    """`Ascii` class that enables common hooks for the `ascii` mode

    Hooks:
        - `_on_screen_resize(self, size: Vec2i) -> None`
        
    """
    root: AsciiEngine

    def _on_screen_resize(self, size: Vec2i) -> None:
        """Override for custom functionality

        Args:
            size (Vec2i): new screen size
        """
        ...


class AsciiNode(Ascii, Node): # Node with Ascii hooks
    """`AsciiNode` with additional hooks related to `ascii` mode functionality

    Hooks:
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """


class AsciiNode2D(Transform2D, AsciiNode): # Node2D with Ascii hooks
    """`AsciiNode2D` with additional hooks related to `ascii` mode functionality

    Hooks:
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """
    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, force_sort: bool = True) -> None:
        """Initializes the 2D node

        Args:
            parent (AnyNode | None, optional): parent node. Defaults to None.
            x (float, optional): local x position. Defaults to 0.
            y (float, optional): local x position. Defaults to 0.
            force_sort (bool, optional): whether to sort based on 'z_index' and 'process_priority'. Defaults to True.
        """
