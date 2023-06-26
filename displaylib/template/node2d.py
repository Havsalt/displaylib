from __future__ import annotations

from ..math import Vec2
from .node import Node
from .transform import Transform2D


class Node2D(Transform2D, Node):
    """`Node2D` class with transform attributes

    Components:
        `Transform2D`: provides transform attributes
    """
    def __init__(self, parent: Node | None = None, *, x: int | float = 0, y: int | float = 0, force_sort: bool = True) -> None:
        super().__init__(parent, force_sort=force_sort) # parameters `x` and `y` is set in `Transform`
        self.position = Vec2(x, y)
