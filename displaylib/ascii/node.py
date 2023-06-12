from __future__ import annotations

from typing import TYPE_CHECKING

from ..template import Node, Node2D

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


class AsciiNode(Ascii, Node): # a variant of the Node
    """`AsciiNode` with additional hooks related to `ascii` mode functionality

    Hooks:
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """


class AsciiNode2D(Ascii, Node2D): # a variant of the Node2D
    """`AsciiNode2D` with additional hooks related to `ascii` mode functionality

    Hooks:
        - `_on_screen_resize(self, size: Vec2i) -> None`
    """
