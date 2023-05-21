from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from ...math import Vec2
from ..node import ASCIINode2D
from ..texture import Texture

if TYPE_CHECKING:
    from ...template import Node


class ASCIIPoint2D(Texture, ASCIINode2D):
    """Thin wrapper around `ASCIINode2D` capable of displaying a single point
    
    Components:
        `Texture`: allows the node to be shown
    """
    def __new__(cls, *args, texture: str = "#", **kwargs): # pulling: `texture`
        return super().__new__(*args, **kwargs)

    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, *, texture: str = "#", force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.texture = [[texture]]


class ASCIILine(ASCIINode2D):
    """Prefabricated `Line` node

    Known issue: Does not work well when changing `rotation` or `global_rotation`
    """
    texture_default: ClassVar[str] = "#" # only used when creating a line node

    def __new__(cls, *args, start: Vec2 = Vec2(0, 0), end: Vec2 = Vec2(0, 0), texture: str | None = None, **kwargs): # pulling: `start`, `end`, `texture`
        return super().__new__(*args, **kwargs)

    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, *, start: Vec2 = Vec2(0, 0), end: Vec2 = Vec2(0, 0), texture: str | None = None, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.start = start
        self.end = end
        self.texture = texture or self.texture_default
        self.z_index = z_index
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
        # -- create points along the current/new line
        diff = (self.end - self.start)
        direction = diff.normalized()
        length = diff.length() # length of difference
        steps = round(length)
        for idx in range(steps):
            position = self.start + (direction * idx)
            point = ASCIIPoint2D(self, x=int(position.x), y=int(position.y), texture=self.texture, z_index=self.z_index)
            self.points.append(point)
    
    def queue_free(self) -> None:
        """Queues all points for deletion before calling its super().queue_free()
        """
        for point in self.points:
            point.queue_free()
        self.points.clear()
        super().queue_free()
