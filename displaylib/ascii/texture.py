from __future__ import annotations

from typing import TypeVar, ClassVar

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
    visible: bool

    def __new__(cls: type[Self], *args, texture: list[list[str]] = [], z_index: int = 0, force_sort: bool = True, **kwargs) -> Self:
        instance = super().__new__(cls, *args, force_sort=force_sort, **kwargs) # `force_sort` is passed to Node eventually
        if not isinstance(instance, Transform2D):
            raise TypeError(f"in class '{instance.__class__.__qualname__}': mixin class '{__class__.__qualname__}' requires to be used in combination with a node class deriving from 'Transform2D'")
        if not getattr(instance, "texture", False):
            setattr(instance, "texture", list())
        setattr(instance, "_z_index", z_index)
        if force_sort:
            Texture._request_z_index_sort = True
        Texture._instances.append(instance)
        return instance
    
    @property
    def z_index(self) -> int:
        return self._z_index

    @z_index.setter
    def z_index(self, value: int) -> None:
        if self._z_index != value: # if changed
            self._z_index = value
            Texture._request_z_index_sort = True

    def queue_free(self) -> None:
        """Decrements this node's reference by removing it from `Texture._instances`.
        Then queues the node to be deleted by the engine
        """
        if self in Texture._instances:
            Texture._instances.remove(self)
        super().queue_free() # called on an instance deriving from Node
