from __future__ import annotations

import copy
from typing import TypeVar, ClassVar

from ..math import Vec2
from ..template import Transform2D

Self = TypeVar("Self")


class Texture: # Component (mixin class)
    """`Texture` mixin class for adding `ASCII graphics` to a node class

    Requires Components:
        - `Transform2D`: uses position and rotation to place the texture
    """
    _instances: ClassVar[list[Texture]] = [] # references to nodes with Texture component
    _request_z_index_sort: ClassVar[bool] = False # requests Engine to sort
    texture: list[list[str]]
    offset: Vec2
    centered: bool

    def __new__(cls: type[Self], *args, texture: list[list[str]] = [], offset: Vec2 = Vec2(0, 0), centered: bool = False, z_index: int = 0, force_sort: bool = True, **kwargs) -> Self:
        instance = super().__new__(cls, *args, force_sort=force_sort, **kwargs) # `force_sort` is passed to Node eventually
        if not isinstance(instance, Transform2D):
            raise TypeError(f"class '{__class__.__qualname__}' is required to derive from 'Transform2D' as it derives from 'Texture'")
        # set if not defined in class
        if not getattr(instance, "texture", False):
            setattr(instance, "texture", texture)
        # set anyway
        setattr(instance, "offset", Vec2(offset.x, offset.y))
        setattr(instance, "centered", centered)
        setattr(instance, "_z_index", z_index)
        if force_sort:
            Texture._request_z_index_sort = True
        Texture._instances.append(instance)
        return instance
    
    @property
    def z_index(self) -> int:
        """Returns the z_index of this node

        Returns:
            int: z_index
        """
        return self._z_index

    @z_index.setter
    def z_index(self, value: int) -> None:
        """Sets the `.z_index` and requests the engine to sort textured nodes based on this

        Args:
            value (int): new z_index
        """
        if self._z_index != value: # if changed
            self._z_index = value
            Texture._request_z_index_sort = True
    
    def get_texture_global_position(self) -> Vec2:
        """Calculates where the texture starts, after taking `.offset` into consideration (world space)

        Returns:
            Vec2: global position of the texture
        """
        global_position = self.position + self.offset
        if self.centered:
            global_position.x -= len(max(self.texture, key=len)) // 2
            global_position.y -= len(self.texture) // 2
        parent = self.parent
        while parent is not None and isinstance(parent, Transform2D):
            global_position = parent.position + global_position.rotated(parent.rotation)
            parent = parent.parent
        return global_position

    def make_unique(self) -> None:
        """Makes a deepcopy of `.texture`, which is then set as the new texture
        """
        self.texture = copy.deepcopy(self.texture) # from class var to instance var (if class var defined)
    
    def as_unique(self: Self) -> Self:
        """Makes a deepcopy of `.texture`, which is then set as the new texture,
        along returning itself

        Returns:
            Self: itself after texture is made unique
        """
        getattr(self, "make_unique")()
        return self

    def queue_free(self) -> None:
        """Decrements the reference of the node by removing it from `Texture._instances`
        and then adds it to the deletion queue of the engine
        """
        if self in Texture._instances:
            Texture._instances.remove(self)
        super().queue_free() # called on an instance deriving from Node
