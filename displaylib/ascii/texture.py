from __future__ import annotations


from ..template import Node2D


class Texture: # Component (mixin class)
    texture: list[list[str]] # type hint
    visible: bool
    _instances = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        if not isinstance(instance, Node2D):
            raise TypeError(f"in class '{instance.__class__.__qualname__}': mixin class '{__class__.__qualname__}' requires to be used in combination with a node class deriving from 'Node2D'")
        setattr(instance, "texture", list())
        Texture._instances.append(instance)
        return instance

    def queue_free(self) -> None:
        if self in Texture._instances:
            Texture._instances.remove(self)
        super().queue_free()
