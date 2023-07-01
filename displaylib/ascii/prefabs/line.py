from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from ...math import Vec2
from ...util import pull
from ..node import AsciiNode2D
from ..texture import Texture

if TYPE_CHECKING:
    from ...template import Node


class AsciiPoint2D(Texture, AsciiNode2D):
    """Thin wrapper around `AsciiNode2D` capable of displaying a single point
    
    Components:
        `Texture`: allows the node to be shown
    """
    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, texture: list[list[str]] = [["#"]], z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.texture = texture
        self.z_index = z_index


@pull("start", "end")
class AsciiLine(AsciiNode2D):
    """Prefabricated `AsciiLine` node

    Known Issues:
        - `Does not work well when changing '.rotation' or using '.set_global_rotation()'`
    """
    texture_default: ClassVar[list[list[str]]] = [["#"]] # only used when creating a line node
    points: list[AsciiPoint2D]

    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, start: Vec2 = Vec2(0, 0), end: Vec2 = Vec2(0, 0), texture: list[list[str]] = texture_default, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.z_index = z_index
        self.force_sort = force_sort
        self.start = start
        self.end = end
        self.texture = texture
        global_position = self.get_global_position()
        self.points: list[AsciiPoint2D] = [
            AsciiPoint2D(self, texture=self.texture, z_index=self.z_index, force_sort=force_sort).where(position=global_position+start),
            AsciiPoint2D(self, texture=self.texture, z_index=self.z_index, force_sort=force_sort).where(position=global_position+end)
        ]
        self._update(0) # simulate initial frame locally

    def _update(self, delta: float) -> None:
        # clear points
        for point in self.points:
            point.queue_free()
        self.points.clear()
        
        if not self.visible:
            return

        global_position = self.get_global_position()
        # creating new ends of line
        self.points: list[AsciiPoint2D] = [
            AsciiPoint2D(self, texture=self.texture, z_index=self.z_index, force_sort=self.force_sort).where(position=global_position+self.start),
            AsciiPoint2D(self, texture=self.texture, z_index=self.z_index, force_sort=self.force_sort).where(position=global_position+self.end)
        ]
        # create points along the current/new line
        diff = (self.end - self.start)
        direction = diff.normalized()
        length = diff.length() # distance determined by difference
        steps = round(length)
        for idx in range(steps):
            offset = self.start + (direction * idx)
            position = global_position + offset
            point = AsciiPoint2D(self, x=int(position.x), y=int(position.y), texture=self.texture, z_index=self.z_index, force_sort=self.force_sort)
            self.points.append(point)
    
    def queue_free(self) -> None:
        """Queues all points for deletion before calling super().queue_free()
        """
        for point in self.points:
            point.queue_free()
        self.points.clear()
        super().queue_free()
