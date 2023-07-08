from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from ..util import pull
from ..template import Node
from .node import AsciiNode2D

if TYPE_CHECKING:
    from ..math import Vec2

Self = TypeVar("Self")


@pull("follow", "mode")
class AsciiCamera(AsciiNode2D):
    """`AsciiCamera` for moving the viewport

    Hooks:
        - `_on_screen_resize(self, size: Vec2i) -> None`
    
    ModeFlags for attribute `mode`: (combined using '|')
        - 0x0 `FIXED` (Default)
        - 0x1 `CENTERED`
        - 0x2 `INCLUDE_SIZE`
    """
    FIXED: ClassVar[int] = 0x0
    CENTERED: ClassVar[int] = 0x1
    INCLUDE_SIZE: ClassVar[int] = 0x2
    current: ClassVar[AsciiCamera]

    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, follow: bool = True, mode: int = FIXED) -> None:
        """Creates a new camera (initially inactive), which can be set active using `.set_current()` or `.as_current()`

        Args:
            parent (Node | None, optional): the parent the camera is attached to. Defaults to None.
            x (int, optional): local x position. Defaults to 0.
            y (int, optional): local y position. Defaults to 0.
            follow (bool, optional): whether to follow parent. Defaults to True.
            mode (int, optional): camera rendering mode (ored together using '|'). Defaults to FIXED.
        """
        super().__init__(parent, x=x, y=y, force_sort=True)
        self.mode = mode # `centered` mode only has effect if `parent` is not None
        self.follow = follow # whether to follow the `parent`
    
    def get_global_position(self) -> Vec2:
        """Computes the node's global position (world space)

        Ignores ancestors' rotation and position if `.follow = False`

        Returns:
            Vec2: global position
        """
        if not self.follow and self.parent is not None:
            return self.position
        return super().get_global_position()

    def get_global_rotation(self) -> float:
        """Computes the node's global rotation (world space)

        Ignores ancestors' rotation if `.follow = False`

        Returns:
            float: global rotation in radians
        """
        if not self.follow and self.parent is not None:
            return self.rotation
        return super().get_global_rotation()
    
    def set_current(self) -> None:
        """Sets this camera as the currently active one
        """
        AsciiCamera.current = self
    
    def as_current(self: Self) -> Self:
        """Sets this camera as the currently active one,
        along returning itself

        Returns:
            Self: itself after set as current camera
        """
        getattr(self, "set_current")()
        return self
