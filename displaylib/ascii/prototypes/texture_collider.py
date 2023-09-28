from __future__ import annotations

from typing import ClassVar, cast

from displaylib.math import Vec2
from displaylib.template.type_hints import MroNext, NodeType


class TextCollider: # Component (mixin class)
    _colliders: ClassVar[list[TextCollider]] = []
    
    def __new__(cls: type[NodeType], *args, **kwargs) -> NodeType:
        mro_next = cast(MroNext[TextCollider], super())
        instance = mro_next.__new__(cls, *args, **kwargs)
        TextCollider._colliders.append(instance)
        return cast(NodeType, instance)

    def move_and_collide(self, distance: Vec2) -> None:
        old_position = self.position.copy()
        self.position += distance
        if collider := self.get_collider():
            self.position = old_position
            self.position.y = collider._get_texture_global_position().y - self.size().y # type: ignore
    
    def move_and_slide(self, distance: Vec2) -> None:
        old_position = self.position.copy()
        self.position.x += distance.x
        signs = distance.sign()
        if collider := self.get_collider():
            self.position = old_position
            if signs.x == 1:
                self.position.x = collider._get_texture_global_position().x - self.size().x # type: ignore
            elif signs.x == -1:
                self.position.x = collider._get_texture_global_position().x + collider.size().x # type: ignore
        old_position = self.position.copy()
        self.position.y += distance.y
        if collider := self.get_collider():
            self.position = old_position
            if signs.y == 1:
                self.position.y = collider._get_texture_global_position().y - self.size().y # type: ignore
            elif signs.y == -1:
                self.position.y = collider._get_texture_global_position().y + collider.size().y # type: ignore
    
    def is_on_floor(self) -> bool:
        old_position = self.position.copy()
        self.position.y += 1
        on_floor = self.is_colliding()
        self.position = old_position
        return on_floor

    def is_colliding(self) -> bool:
        for collider in TextCollider._colliders:
            if collider is self:
                continue
            elif self.is_colliding_with(collider):
                return True
        return False

    def get_collider(self) -> TextCollider | None:
        for collider in TextCollider._colliders:
            if collider is self:
                continue
            elif self.is_colliding_with(collider):
                return collider
        return None
    
    def get_all_colliders(self) -> list[TextCollider]:
        results: list[TextCollider] = []
        for collider in TextCollider._colliders:
            if collider is self:
                continue
            elif self.is_colliding_with(collider):
                results.append(collider)
        return results
    
    def is_colliding_with(self, other: TextCollider) -> bool:
        # basic implementation
        position = self._get_texture_global_position() # type: ignore
        start = other._get_texture_global_position() # type: ignore
        rect = (start, start + other.size()) # start, end  # type: ignore
        return any( # any intersects
            self._point_intersects_with(point, rect)
            for point in [
                position,
                position + self.size(), # type: ignore
                position + Vec2(self.size().x, 0), # type: ignore
                position + Vec2(0, self.size().y) # type: ignore
            ])

    def _point_intersects_with(self, point: Vec2, rect: tuple[Vec2, Vec2]) -> bool:
        start, end = rect
        x_inside = start.x < point.x < end.x
        y_inside = start.y < point.y < end.y
        return x_inside and y_inside

    def queue_free(self) -> None:
        if self in TextCollider._colliders:
            TextCollider._colliders.remove(self)
        super().queue_free() # type: ignore
