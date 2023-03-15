from __future__ import annotations

from typing import TYPE_CHECKING
from ..template import Node2D

if TYPE_CHECKING:
    import pygame
    from ..template import Node


class PygameNode2D(Node2D):
    __logical__ = False # exists in the "real world"

    def __init__(self, parent: Node | None = None, *, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index, force_sort)
    
    def _input(event: pygame.event.Event) -> None:
        ...
    
    def _render(self, surface: pygame.Surface) -> None:
        ...
