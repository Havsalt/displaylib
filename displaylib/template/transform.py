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
        setattr(instance, "position", Vec2(x, y))
        setattr(instance, "rotation", 0.0)
        # only nodes with Transform2D will have the option to be visible
        setattr(instance, "visible", True) # local visibility
        return instance

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.position.x}, {self.position.y})"
    
    def get_global_position(self) -> Vec2:
        """Computes the node's global position (world space)

        Returns:
            Vec2: global position
        """
        global_position = self.position.copy()
        parent = self.parent
        while parent is not None and isinstance(parent, Transform2D):
            global_position = parent.position + global_position.rotated(parent.rotation)
            parent = parent.parent
        return global_position
    
    def set_global_position(self, position: Vec2) -> None:
        """Sets the node's global position (world space)
        """
        diff = position - self.get_global_position()
        self.position += diff
    
    def get_global_rotation(self) -> float:
        """Computes the node's global rotation (world space)

        Returns:
            float: global rotation in radians
        """
        rotation = self.rotation
        parent = self.parent
        while parent is not None and isinstance(parent, Transform2D):
            rotation += parent.rotation
            parent = parent.parent
        return rotation

    def set_global_rotation(self, rotation: float) -> None:
        """Sets the node's global rotation (world space)
        """
        diff = rotation - self.get_global_rotation()
        self.rotation += diff
    
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

    def hide(self) -> None:
        self.visible = False
    
    def show(self) -> None:
        self.visible = True
    
    def look_at(self, location: Vec2) -> None:
        """Makes the node look in the direction of the supplied location

        Args:
            location (Vec2): point in global space
        """
        diff = location - self.global_position
        angle = diff.angle()
        self.global_rotation = -angle
