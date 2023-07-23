from __future__ import annotations

import copy
from typing import TYPE_CHECKING, ClassVar, cast

from ..math import Vec2, Vec2i
from ..template import Transform2D
from ..template.type_hints import MroNext, NodeType
from .type_hints import NodeMixin, ValidTextureNode, TextureSelf

if TYPE_CHECKING:
    from .type_hints import TextureSelf


class Texture: # Component (mixin class)
    """`Texture` mixin class for adding `ASCII graphics` to a 2D node class

    Requires Components:
        - `Transform2D`: uses position and rotation to place the texture
    """
    _instances: ClassVar[list[ValidTextureNode]] = [] # references to nodes with Texture component
    _request_z_index_sort: ClassVar[bool] = False # requests Engine to sort
    texture: list[list[str]]
    offset: Vec2
    centered: bool
    z_index: int # type: ignore

    def __new__(cls: type[NodeType], *args, texture: list[list[str]] = [], offset: Vec2 = Vec2(0, 0), centered = None, z_index: int = 0, force_sort: bool = True, **kwargs) -> NodeType: # borrowing: `force_sort`
        mro_next = cast(MroNext[ValidTextureNode], super())
        instance = mro_next.__new__(cls, *args, force_sort=force_sort, **kwargs) # `force_sort` is passed to Node eventually
        # override -> class value -> default
        if texture or not hasattr(instance, "texture"):
            instance.texture = texture # class value is shared texture (use `.make_unique()` or `.as_unique()`)
        # override -> class value -> default
        if offset or not hasattr(instance, "offset"):
            instance.offset = offset.copy() # unique offset
        # override -> class value -> default
        if centered is not None:
            instance.centered = centered
        elif not hasattr(instance, "centered"):
            instance.centered = False
        # override -> class value -> default
        if z_index or not hasattr(instance, "_z_index"):
            instance._z_index = z_index
        if force_sort:
            Texture._request_z_index_sort = True
        Texture._instances.append(instance)
        return cast(NodeType, instance)
    
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

    def make_unique(self) -> None:
        """Makes a deepcopy of `.texture`, which is then set as the new texture
        """
        self.texture = copy.deepcopy(self.texture) # from class var to instance var (if class var defined)
    
    def as_unique(self: TextureSelf) -> TextureSelf:
        """Makes a deepcopy of `.texture`, which is then set as the new texture,
        along returning itself

        Returns:
            TextureSelf: itself after texture is made unique
        """
        self.make_unique()
        return self

    def size(self) -> Vec2i:
        """Returns the width and height of `.texture` as a Vec2i, where x=width and y=height

        Returns:
            Vec2i: size of the content
        """
        longest = len(max(self.texture, key=len))
        lines = len(self.texture)
        return Vec2i(longest, lines)

    def queue_free(self) -> None:
        """Decrements the reference of the node by removing it from `Texture._instances`
        and then adds it to the deletion queue of the engine
        """
        if self in Texture._instances:
            Texture._instances.remove(self)
        mro_next = cast(NodeMixin, super())
        mro_next.queue_free()
    
    def _get_texture_global_position(self) -> Vec2:
        """Calculates where the texture starts, after taking `.offset` into consideration (world space)

        Returns:
            Vec2: global position of the texture
        """
        self = cast(ValidTextureNode, self) # fixes type hints
        global_position = self.position + self.offset
        if self.centered: # subtract hald size of the texture
            global_position.x -= len(max(self.texture, key=len)) // 2
            global_position.y -= len(self.texture) // 2
        parent = self.parent
        while parent is not None and isinstance(parent, Transform2D): # global position
            global_position = parent.position + global_position.rotated(parent.rotation)
            parent = parent.parent
        return global_position

    def _get_final_texture(self) -> list[list[str]]:
        """Some components may override this implementation, for example colorizing the texture

        Returns:
            list[list[str]]: here, it is just the original texture
        """
        super_implementation = getattr(super(), "_get_final_texture", None)
        if super_implementation is not None:
            return super_implementation() # usually the Color component implementation
        return self.texture
