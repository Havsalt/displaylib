from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, cast

from ...math import Vec2
from ...template.type_hints import MroNext, NodeType, NodeMixin
from ..node import AsciiNode2D
from ..texture import Texture
from ..colored import Color
from ..color import WHITE

if TYPE_CHECKING:
    from ...template.type_hints import AnyNode
    from ..color import ColorValue


class AsciiPoint2D(Color, Texture, AsciiNode2D):
    """Behaves like an `AsciiSprite`, capable of displaying a single point
    
    Components:
        - `Texture`: allows the node to be shown
        - `Color`: applies color to the texture
    """
    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, texture: list[list[str]] = [["#"]], color: ColorValue = WHITE, z_index: int = 0, force_sort: bool = True) -> None:
        """_summary_

        Args:
            parent (AnyNode | None, optional): _description_. Defaults to None.
            x (float, optional): _description_. Defaults to 0.
            y (float, optional): _description_. Defaults to 0.
            texture (list[list[str]], optional): _description_. Defaults to [["#"]].
            color (ColorValue, optional): _description_. Defaults to WHITE.
            z_index (int, optional): _description_. Defaults to 0.
            force_sort (bool, optional): _description_. Defaults to True.
        """


class AsciiLine(AsciiNode2D):
    """Prefabricated `AsciiLine` node with local start and end point
    """
    texture_default: ClassVar[list[list[str]]] = [["#"]] # only used when creating a line node
    texture: list[list[str]]
    color: ColorValue
    start: Vec2
    end: Vec2
    z_index: int
    force_sort: bool
    points: list[AsciiPoint2D]

    def __new__(cls: type[NodeType], *args, texture: list[list[str]] = texture_default, color = None, start: Vec2 = Vec2(0, 0), end: Vec2 = Vec2(0, 0), z_index: int = 0, force_sort: bool = True, **kwargs) -> NodeType:
        mro_next = cast(MroNext[AsciiLine], super())
        instance = mro_next.__new__(cls, *args, **kwargs)
        # override -> class value -> default
        if color is not None:
            instance.color = color
        if not hasattr(instance, "color"):
            instance.color = WHITE
        # override -> class value -> default
        if texture or not hasattr(instance, "texture"):
            instance.texture = texture # class value is shared texture (use `.make_unique()` or `.as_unique()`)
        # override -> class value -> default
        if start or not hasattr(instance, "start"):
            instance.start = start.copy() # unique start
        # override -> class value -> default
        if end or not hasattr(instance, "end"):
            instance.end = end.copy() # unique end
        # override -> class value -> default
        if z_index or not hasattr(instance, "z_index"):
            instance.z_index = z_index
        # override/default
        if not hasattr(instance, "force_sort"):
            instance.force_sort = force_sort
        # default
        instance.points = []
        instance._update(0)
        return cast(NodeType, instance)

    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, texture: list[list[str]] = texture_default, color: ColorValue = WHITE, start: Vec2 = Vec2(0, 0), end: Vec2 = Vec2(0, 0), z_index: int = 0, force_sort: bool = True) -> None:
        """Initializes the line

        Args:
            parent (AnyNode | None, optional): parent node. Defaults to None.
            x (float, optional): local x position. Defaults to 0.
            y (float, optional): local y position. Defaults to 0.
            texture (list[list[str]], optional): visible texture. Defaults to texture_default.
            color (ColorValue, optional): texture color. Defaults to WHITE.
            start (Vec2, optional): start of the line. Defaults to Vec2(0, 0).
            end (Vec2, optional): end of the line. Defaults to Vec2(0, 0).
            z_index (int, optional): layer to render on. Defaults to 0.
            force_sort (bool, optional): whether to sort based on 'z_index' and 'process_priority'. Defaults to True.
        """
        # super().__init__(parent, x=x, y=y, force_sort=force_sort)
        # these uses class variables as default if set
        # self.texture = texture or getattr(self, "texture", texture)
        # self.color = color if (color != WHITE) else getattr(self, "color", color) # if not defined in class, use default (which may be WHITE)
        # self.start = start or getattr(self, "start", start)
        # self.end = end or getattr(self, "end", end)
        # self.z_index = z_index or getattr(self, "z_index", z_index)
        # self.force_sort = force_sort # only uses override/default
        # self._update(0) # simulate initial frame locally

    def _update(self, _delta: float) -> None:
        # clear points
        for point in self.points:
            point.queue_free()
        self.points.clear()
        
        if not self.is_globally_visible():
            return # do not create points

        # creating new ends of line
        self.points = [
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
        mro_next = cast(NodeMixin, super())
        mro_next.queue_free()
