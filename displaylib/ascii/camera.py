from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, cast

from .node import AsciiNode2D
from ..template.type_hints import MroNext, NodeType

if TYPE_CHECKING:
    from ..math import Vec2
    from ..template.type_hints import AnyNode
    from .type_hints import AsciiCameraSelf


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
    follow: bool
    mode: int

    def __new__(cls: type[NodeType], *args, follow = None, mode: int = 0, **kwargs) -> NodeType:
        mro_next = cast(MroNext[AsciiCamera], super())
        instance = mro_next.__new__(cls, *args, **kwargs)
        # override -> class value -> default
        if follow is not None:
            instance.follow = follow
        elif not hasattr(instance, "follow"):
            instance.follow = False
        # override -> class value -> default
        if mode or not hasattr(instance, "mode"):
            instance.mode = mode
        return cast(NodeType, instance)

    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, follow: bool = True, mode: int = FIXED) -> None:
        """Creates a new camera (initially inactive), which can be set active using `.set_current()` or `.as_current()`

        Args:
            parent (Node | None, optional): the parent the camera is attached to. Defaults to None.
            x (int, optional): local x position. Defaults to 0.
            y (int, optional): local y position. Defaults to 0.
            follow (bool, optional): whether to follow parent. Defaults to True.
            mode (int, optional): camera rendering mode (ored together using '|'). Defaults to FIXED.
        """
    
    def get_global_position(self) -> Vec2:
        """Computes the node's global position (world space)

        Ignores ancestors' rotation and position if `.follow = False`

        Returns:
            Vec2: global position
        """
        if not self.follow or self.parent is not None:
            return self.position
        return super().get_global_position()

    def get_global_rotation(self) -> float:
        """Computes the node's global rotation (world space)

        Ignores ancestors' rotation if `.follow = False`

        Returns:
            float: global rotation in radians
        """
        if not self.follow or self.parent is not None:
            return self.rotation
        return super().get_global_rotation()
    
    def set_current(self) -> None:
        """Sets this camera as the currently active one
        """
        AsciiCamera.current = self
    
    def as_current(self: AsciiCameraSelf) -> AsciiCameraSelf:
        """Sets this camera as the currently active one,
        along returning itself

        Returns:
            AsciiCameraSelf: itself after set as current camera
        """
        self.set_current()
        return self
    
    def is_current(self) -> bool:
        """Returns whether this camera is the currently active camera

        Returns:
            bool: state
        """
        return AsciiCamera.current is self
