from typing_extensions import Self
from ..template import Node2D
from .types import Event, Surface


class PygameNode(Node2D):
    __logical__ = False # exists in the "real world"

    def __init__(self, parent: Self | None = None, *, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index, force_sort)
    
    def _input(event: Event) -> None:
        return
    
    def _render(self, surface: Surface) -> None:
        return
