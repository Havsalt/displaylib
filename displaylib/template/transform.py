from __future__ import annotations

from typing import TypeVar

from ..math import Vec2

Self = TypeVar("Self")


class Transform2D: # Component (mixin class)
    """`Transform2D` mixin class for adding position, rotation and visibility to a node class
    """
    position: Vec2
    rotation: float
    visible: bool

    def __new__(cls: type[Self], *args, x: int | float = 0, y: int | float = 0, **kwargs) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        setattr(instance, "position",  Vec2(x, y))
        setattr(instance, "rotation", 0.0)
        # only nodes with Transform2D will have the option to be visible
        setattr(instance, "visible", True) # local visibility
        return instance

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.position.x}, {self.position.y})"
    
    @property
    def global_position(self) -> Vec2:
        position = self.position
        parent = self.parent
        while parent is not None and isinstance(parent, Transform2D):
            position += parent.position.rotated(parent.rotation)
            parent = parent.parent
        return position
    
    @global_position.setter
    def global_position(self, position: Vec2) -> None:
        diff = position - self.global_position
        self.position += diff
    
    @property
    def global_rotation(self) -> float:
        rotation = self.rotation
        parent = self.parent
        while parent is not None and isinstance(parent, Transform2D):
            rotation += parent.rotation
            parent = parent.parent
        return rotation

    @global_rotation.setter
    def global_rotation(self, rotation: float) -> None:
        diff = rotation - self.global_rotation
        self.rotation += diff
    
    @property
    def is_globally_visible(self) -> bool: # global visibility
        if not self.visible:
            return False
        parent = self.parent
        while parent != None:
            if not isinstance(parent, Transform2D):
                return True
            if not parent.visible:
                return False
            parent = parent.parent
        return True
    
    def look_at(self, location: Vec2) -> None:
        diff = location - self.global_position
        angle = diff.angle()
        self.global_rotation = -angle
