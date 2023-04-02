from __future__ import annotations


from ..template import Node2D


class Texture: # Component (mixin class)
    """`Texture` mixin class for adding ASCII graphics to a node class
    """
    texture: list[list[str]]
    visible: bool
    _instances: list[Texture] = [] # nodes with Texture component

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        if not isinstance(instance, Node2D):
            raise TypeError(f"in class '{instance.__class__.__qualname__}': mixin class '{__class__.__qualname__}' requires to be used in combination with a node class deriving from 'Node2D'")
        setattr(instance, "texture", list())
        Texture._instances.append(instance)
        return instance

    def queue_free(self) -> None:
        """Decrements this node's reference by removing it from `Texture._instances`.
        Then queues the node to be deleted by the engine
        """
        if self in Texture._instances:
            Texture._instances.remove(self)
        super().queue_free() # called on an instance deriving from Node
