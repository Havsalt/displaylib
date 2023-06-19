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
    
    Optional Hooks:
        - `_on_mouse_event(self, event: MouseEvent) -> None`
    
    ModeFlags for attribute `mode`:
        - 1 `FIXED` (Default)
        - 3 `CENTERED`
        - 5 `INCLUDE_SIZE`
        - 8 `CENTERED_AND_INCLUDE_SIZE` (`CENTERED + INCLUDE_SIZE`)
    
    Any invalid flag combination will be treated as `FIXED` (1)
    """
    FIXED: ClassVar[int] = 1
    CENTERED: ClassVar[int] = 3
    INCLUDE_SIZE: ClassVar[int] = 5
    CENTERED_AND_INCLUDE_SIZE: ClassVar[int] = 8
    current: ClassVar[AsciiCamera]

    def __init__(self, parent: Node | None = None, *, x: int = 0, y: int = 0, follow: bool = True, mode: int = FIXED) -> None:
        """Creates a new camera (initially inactive), which can be set active using `.set_current()` or `.as_current()`

        Args:
            parent (Node | None, optional): the parent the camera is attached to. Defaults to None.
            x (int, optional): local x position. Defaults to 0.
            y (int, optional): local y position. Defaults to 0.
            follow (bool, optional): whether to follow parent. Defaults to True.
            mode (int, optional): camera rendering mode. Defaults to FIXED.
        """
        super().__init__(parent, x=x, y=y, force_sort=True)
        self.mode = mode # `centered` mode only has effect if `parent` is not None
        self.follow = follow # whether to follow the `parent`
    
    @property
    def global_position(self) -> Vec2:
        """Computes the node's global position (world space)

        Ignores ancestors' rotation and position if `.follow = False`

        Returns:
            Vec2: global position
        """
        if not self.follow and self.parent is not None:
            return self.position
        return super().global_position

    @property
    def global_rotation(self) -> float:
        """Computes the node's global rotation (world space)

        Ignores ancestors' rotation if `.follow = False`

        Returns:
            float: global rotation in radians
        """
        if not self.follow and self.parent is not None:
            return self.rotation
        return super().global_rotation
    
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
