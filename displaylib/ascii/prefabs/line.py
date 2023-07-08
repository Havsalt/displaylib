from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from ...math import Vec2
from ...util import pull
from ..node import AsciiNode2D
from ..texture import Texture
from ..colored import Color
from ..color import WHITE, _Color

if TYPE_CHECKING:
    from ...template import Node


class AsciiPoint2D(Color, Texture, AsciiNode2D):
    """Thin wrapper around `AsciiNode2D` capable of displaying a single point
    
    Components:
        - `Texture`: allows the node to be shown
        - `Color`: applies color to the texture
    """
    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, texture: list[list[str]] = [["#"]], color: _Color = WHITE, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.texture = texture
        self.color = color
        self.z_index = z_index


@pull("color", "start", "end")
class AsciiLine(AsciiNode2D):
    """Prefabricated `AsciiLine` node
    """
    texture_default: ClassVar[list[list[str]]] = [["#"]] # only used when creating a line node
    points: list[AsciiPoint2D]

    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, color: _Color = WHITE, texture: list[list[str]] = texture_default, start: Vec2 = Vec2(0, 0), end: Vec2 = Vec2(0, 0), z_index: int = 0, force_sort: bool = True) -> None:
        """Initializes the line

        Args:
            parent (Node | None, optional): parent node. Defaults to None.
            x (float, optional): local x position. Defaults to 0.
            y (float, optional): local y position. Defaults to 0.
            texture (list[list[str]], optional): visible texture. Defaults to texture_default.
            color (_Color, optional): texture color. Defaults to WHITE.
            start (Vec2, optional): start of the line. Defaults to Vec2(0, 0).
            end (Vec2, optional): end of the line. Defaults to Vec2(0, 0).
            z_index (int, optional): layer to render on. Defaults to 0.
            force_sort (bool, optional): whether to sort based on 'z_index' and 'process_priority'. Defaults to True.
        """
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.texture = texture
        self.color = color
        self.start = start
        self.end = end
        self.z_index = z_index
        self.force_sort = force_sort
        self.points: list[AsciiPoint2D] = []
        self._update(0) # simulate initial frame locally

    def _update(self, _delta: float) -> None:
        # clear points
        for point in self.points:
            point.queue_free()
        self.points.clear()
        
        if not self.is_globally_visible():
            return # do not create points

        # creating new ends of line
        self.points: list[AsciiPoint2D] = [
            AsciiPoint2D(self, texture=self.texture, color=self.color, z_index=self.z_index, force_sort=self.force_sort).where(position=self.start),
            AsciiPoint2D(self, texture=self.texture, color=self.color, z_index=self.z_index, force_sort=self.force_sort).where(position=self.end)
        ]
        # create points along the current/new line
        diff = (self.end - self.start)
        direction = diff.normalized()
        length = diff.length() # distance determined by difference
        steps = round(length)
        for idx in range(steps):
            position = self.start + (direction * idx)
            point = AsciiPoint2D(self, x=int(position.x), y=int(position.y), texture=self.texture, color=self.color, z_index=self.z_index, force_sort=self.force_sort)
            self.points.append(point)
    
    def queue_free(self) -> None:
        """Queues all points for deletion before calling super().queue_free()
        """
        for point in self.points:
            point.queue_free()
        self.points.clear()
        super().queue_free()
