from __future__ import annotations

from typing import cast

from ..math import Vec2
from .type_hints import MroNext, ValidTransform2DNode, Transform2DMixin, Self


class Transform2D: # Component (mixin class)
    """`Transform2D` mixin class for adding position, rotation and visibility to a node class
    """
    position: Vec2
    rotation: float
    visible: bool

    def __new__(cls: type[Self], *args, x: float = 0, y: float = 0, **kwargs) -> Self:
        mro_next = cast(MroNext[ValidTransform2DNode], super())
        instance = mro_next.__new__(cast(type[Transform2DMixin], cls), *args, **kwargs)
        instance.position = Vec2(x, y)
        instance.rotation = 0.0
        # only nodes with Transform2D component will have the option to be visible
        instance.visible = True # local visibility
        return cast(Self, instance)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.position.x}, {self.position.y})"
    
    def get_global_position(self) -> Vec2:
        """Computes the node's global position (world space)

        Returns:
            Vec2: global position
        """
        self = cast(ValidTransform2DNode, self) # fixes type hinting
        global_position = self.position.copy()
        parent = self.parent
        while parent is not None and isinstance(parent, Transform2D):
            global_position = parent.position + global_position.rotated(parent.rotation)
            parent = parent.parent
        return global_position
    
    def set_global_position(self, position: Vec2) -> None:
        """Sets the node's global position (world space)
        """
        self = cast(ValidTransform2DNode, self) # fixes type hinting
        diff = position - self.get_global_position()
        self.position += diff
    
    def get_global_rotation(self) -> float:
        """Computes the node's global rotation (world space)

        Returns:
            float: global rotation in radians
        """
        self = cast(ValidTransform2DNode, self) # fixes type hinting
        rotation = self.rotation
        parent = self.parent
        while parent is not None and isinstance(parent, Transform2D):
            rotation += parent.rotation
            parent = parent.parent
        return rotation

    def set_global_rotation(self, rotation: float) -> None:
        """Sets the node's global rotation (world space)
        """
        self = cast(ValidTransform2DNode, self) # fixes type hinting
        diff = rotation - self.get_global_rotation()
        self.rotation += diff
    
    def is_globally_visible(self) -> bool: # global visibility
        """Checks whether the node and its ancestors are visible

        Returns:
            bool: global visibility
        """
        self = cast(ValidTransform2DNode, self) # fixes type hinting
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
        self = cast(ValidTransform2DNode, self) # fixes type hinting
        diff = location - self.get_global_position()
        angle = diff.angle()
        self.set_global_rotation(-angle)
