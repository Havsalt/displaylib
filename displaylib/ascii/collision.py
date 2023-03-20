from __future__ import annotations

from ..template import Component
from .node import ASCIINode2D


class CollisionShape2D(ASCIINode2D):
    ...


class Collider(Component):
    _colliders = []
    
    def _init(self, *args, **kwargs) -> None:
        ...
    
    def free(self) -> None:
        Collider._colliders.remove(self)
        super().free()
