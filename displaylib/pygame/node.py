from __future__ import annotations

from typing import TYPE_CHECKING
from ..template import Node2D

if TYPE_CHECKING:
    import pygame
    from ..template import Node


class PygameNode2D(Node2D):
    """`PygameNode2D` with additional hooks from Node2D

    Hooks:
        `_input(self, event: pygame.event.Event) -> None`
        `_render(self, surface: pygame.Surface) -> None`
    """
    def __init__(self, parent: Node | None = None, *, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index=z_index, force_sort=force_sort)
    
    def _input(self, event: pygame.event.Event) -> None:
        """Override for custom functionality

        Args:
            event (pygame.event.Event): event received
        """
        ...
    
    def _render(self, surface: pygame.Surface) -> None:
        """Override for custom functionality

        Args:
            surface (pygame.Surface): surface to render custom content onto
        """
        ...
