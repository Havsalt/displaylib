from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from ..math import Vec2i
from ..template import Node
from .node import AsciiNode2D

if TYPE_CHECKING:
    from .surface import AsciiSurface

Self = TypeVar("Self")


class AsciiCamera(AsciiNode2D):
    """`AsciiCamera` for moving the viewport

    Hooks:
        - `_render(self, surface: AsciiSurface) -> None`
        - `_on_screen_resize(self, size: Vec2i) -> None`
    
    ModeFlags for attribute `mode`:
        - 1 `FIXED` (Default)
        - 3 `CENTERED`
        - 5 `INCLUDE_SIZE`
        - 8 `CENTERED_AND_INCLUDE_SIZE` (`CENTERED + INCLUDE_SIZE`)
    
    Any invalid flag combination will be treated as `FIXED` (1)
    """
    FIXED = 1
    CENTERED = 3
    INCLUDE_SIZE = 5
    CENTERED_AND_INCLUDE_SIZE = 8
    current: ClassVar[AsciiCamera]

    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, *, follow: bool = False, mode: int = FIXED) -> None:
        super().__init__(parent, x=x, y=y, force_sort=True)
        self.mode = mode # `centered` mode only has effect if `parent` is not None
        self.follow = follow # whether to follow the `parent`
    
    def _render(self, surface: AsciiSurface) -> None:
        """Override for custom functionality

        Args:
            surface (AsciiSurface): surface to blit onto
        """
        ...

    def _on_screen_resize(self, size: Vec2i) -> None:
        """Override for custom functionality

        Args:
            size (Vec2i): the new screen size
        """
        ...
    
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
