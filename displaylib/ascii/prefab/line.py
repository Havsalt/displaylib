from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from ...math import Vec2
from ...util import pull
from ..node import ASCIINode2D
from ..texture import Texture

if TYPE_CHECKING:
    from ...template import Node


@pull("texture", "z_index")
class ASCIIPoint2D(Texture, ASCIINode2D):
    """Thin wrapper around `ASCIINode2D` capable of displaying a single point
    
    Components:
        `Texture`: allows the node to be shown
    """
    def __init__(self, parent: Node | None = None, *, x: int = 0, y: int = 0, texture: str = "#", z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.texture = [[texture]]
        self.z_index = z_index


@pull("start", "end", "texture", "z_index")
class ASCIILine(ASCIINode2D):
    """Prefabricated `ASCIILine` node

    Known Issues:
        - `Does not work well when changing '.rotation' or '.global_rotation'`
    """
    texture_default: ClassVar[str] = "#" # only used when creating a line node

    def __init__(self, parent: Node | None = None, *, x: int = 0, y: int = 0, start: Vec2 = Vec2(0, 0), end: Vec2 = Vec2(0, 0), texture: str = texture_default, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.z_index = z_index
        self.force_sort = force_sort
        self.start = start
        self.end = end
        self.texture = texture
        self.points: list[ASCIIPoint2D] = [
            ASCIIPoint2D(self, texture=self.texture, z_index=self.z_index, force_sort=force_sort).where(position=start),
            ASCIIPoint2D(self, texture=self.texture, z_index=self.z_index, force_sort=force_sort).where(position=end)
        ]
        self._update(0) # simulate initial frame locally

    def _update(self, delta: float) -> None:
        # clear points
        for point in self.points:
            point.queue_free()
        self.points.clear()
        
        if not self.visible:
            return

        # creating new ends of line
        self.points: list[ASCIIPoint2D] = [
            ASCIIPoint2D(self, texture=self.texture, z_index=self.z_index, force_sort=self.force_sort).where(position=self.start),
            ASCIIPoint2D(self, texture=self.texture, z_index=self.z_index, force_sort=self.force_sort).where(position=self.end)
        ]
        # create points along the current/new line
        diff = (self.end - self.start)
        direction = diff.normalized()
        length = diff.length() # distance determined by difference
        steps = round(length)
        for idx in range(steps):
            position = self.start + (direction * idx)
            point = ASCIIPoint2D(self, x=int(position.x), y=int(position.y), texture=self.texture, z_index=self.z_index, force_sort=self.force_sort)
            self.points.append(point)
    
    def queue_free(self) -> None:
        """Queues all points for deletion before calling super().queue_free()
        """
        for point in self.points:
            point.queue_free()
        self.points.clear()
        super().queue_free()
