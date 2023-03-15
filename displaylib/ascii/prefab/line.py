from __future__ import annotations

from typing import TYPE_CHECKING

from ...math import Vec2
from ..node import ASCIINode2D

if TYPE_CHECKING:
    from ...template import Node


class ASCIIPoint2D(ASCIINode2D):
    """Thin wrapper around `ASCIINode2D`
    """
    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, texture: str = "#", z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index, force_sort)
        self.content = [[texture]]


class ASCIILine(ASCIINode2D):
    """Prefabricated `Line` node

    Known issue: Does not work well when changing `rotation` or `global_rotation`
    """
    texture_default: str = "#" # only used when creating a line node

    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, start: Vec2 = Vec2(0, 0), end: Vec2 = Vec2(0, 0), texture: str = "", z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index, force_sort)
        self.start = start
        self.end = end
        self.texture = self.texture_default if texture == "" else texture
        self.points: list[ASCIIPoint2D] = [
            ASCIIPoint2D(self, z_index=self.z_index, texture=self.texture).where(position=start),
            ASCIIPoint2D(self, z_index=self.z_index, texture=self.texture).where(position=end)
        ]

    def _update(self, delta: float) -> None:
        # -- clear points
        for point in self.points:
            point.queue_free()
        self.points.clear()

        if not self.visible:
            return

        diff = (self.end - self.start)
        normalized = diff.normalized()
        length = diff.length() # length of difference
        steps = round(length)
        for idx in range(steps):
            position = self.start + (normalized * idx)
            point = ASCIIPoint2D(self, x=int(position.x), y=int(position.y), texture=self.texture, z_index=self.z_index)
            self.points.append(point)
    
    def queue_free(self) -> None:
        for point in self.points:
            point.queue_free()
        self.points.clear()
        super().queue_free()