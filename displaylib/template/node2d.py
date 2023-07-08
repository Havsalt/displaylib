from __future__ import annotations

from ..math import Vec2
from .node import Node
from .transform import Transform2D


class Node2D(Transform2D, Node):
    """`Node2D` class with transform attributes

    Components:
        `Transform2D`: provides position and rotation attributes
    """
    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, force_sort: bool = True) -> None:
        """Initializes the node in 2D space

        Args:
            parent (Node | None, optional): parent node. Defaults to None.
            x (float, optional): local x position. Defaults to 0.
            y (float, optional): local y position. Defaults to 0.
            force_sort (bool, optional): whether to sort based on 'z_index' and 'process_priority'. Defaults to True.
        """
        super().__init__(parent, force_sort=force_sort) # parameters `x` and `y` is set in `Transform`
        self.position = Vec2(x, y)
