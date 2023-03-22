from __future__ import annotations

from typing import TYPE_CHECKING

from ..math import Vec2

if TYPE_CHECKING:
    from .engine import Engine


class NodePriorityMeta(type):
    """Node metaclass for initializing `Node` subclass before other `mixin` classes
    """
    @staticmethod
    def _mixin_sort(base: type) -> bool:
        return not issubclass(base, Node)

    def __new__(cls, name: str, bases: tuple[type], dct: dict[str, object]):
        sorted_bases = tuple(sorted(bases, key=NodePriorityMeta._mixin_sort))
        return super().__new__(cls, name, sorted_bases, dct)


class Node(metaclass=NodePriorityMeta):
    """Node base class

    Automatically keeps track of alive Node(s) by reference.
    An Engine subclass may access it's nodes through the `nodes` class attribute
    """
    root: Engine # set from a Engine subclass
    nodes: dict[int, Node] = {} # all nodes that are alive
    _request_sort: bool = False # requests Engine to sort
    _queued_nodes: set[Node] = set() # uses <Node>.queue_free() to ask Engine to delete them

    def __new__(cls: type[Node], *args, **kwargs) -> Node:
        """In addition to default behaviour, automatically store the node in a dict.
        Keeps the object alive by the reference stored

        Args:
            cls (type[Node]): class of the node being created

        Returns:
            Node: node instance that was stored
        """
        instance = super().__new__(cls)
        Node.nodes[id(instance)] = instance
        return instance

    def __init__(self, parent: Node | None = None, *, force_sort: bool = True) -> None:
        self.parent = parent
        self.z_index = 0
        if force_sort: # if True, requests sort every frame a new node is created
            Node._request_sort = True # otherwise, depent on a `z_index` change

    def __repr__(self) -> str:
        """Returns a default representation of the Node object

        Returns:
            str: node representation
        """
        return f"<{self.__class__.__qualname__} object at {hex(id(self))}>"

    def __str__(self) -> str:
        """Returns a default string representation of the Node object

        Returns:
            str: node representation
        """
        return f"{self.__class__.__name__}()"
    
    @property
    def name(self) -> str:
        """Returns class name

        Returns:
            str: class name
        """
        return self.__class__.__name__

    def where(self, **attributes) -> Node:
        """Sets/overrides the given attributes the node instance

        Returns:
            Node: self after modification(s)
        """
        for key, value in attributes.items():
            setattr(self, key, value)
        return self

    def _update(self, delta: float) -> None:
        """Called every frame by the Engine class
        
        Override for custom functionality

        Args:
            delta (float): time since last frame
        """
        ...
    
    def queue_free(self) -> None:
        """Tells the Engine to `delete` this <Node> after
        every node has been called `_update` on
        """
        Node._queued_nodes.add(self)


class Node2D(Node):
    """Node2D class with transform attributes
    """
    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        self._z_index = z_index # has to be before Node init
        super().__init__(parent, force_sort=force_sort)
        self.parent = parent
        self.position = Vec2(x, y)
        self.rotation = 0.0
        self.visible = True # only nodes on the 2D plane will have the option to be visible
        if force_sort: # if True, requests sort every frame a new node is created
            Node._request_sort = True # otherwise, depend on a `z_index` change
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.position.x}, {self.position.y})"

    @property
    def z_index(self) -> int:
        return self._z_index

    @z_index.setter
    def z_index(self, value: int) -> None:
        if self._z_index != value:
            self._z_index = value
            Node._request_sort = True
    
    @property
    def global_position(self) -> Vec2:
        linear_segments = [] # top parent -> branches -> leaf
        position = self.position
        current = self
        parent = self.parent
        while parent != None:
            if not isinstance(parent, Node2D):
                break
            # -- do stuff
            position += current.position.rotated_around(current.rotation, parent.position)
            # -- end
            current, parent = parent, parent.parent
        return position
    
    @global_position.setter
    def global_position(self, position: Vec2) -> None:
        diff = position - self.global_position
        self.position += diff
    
    @property
    def global_rotation(self) -> float:
        rotation = self.rotation
        node = self.parent
        while node != None:
            if not isinstance(node, Node2D):
                break
            rotation += node.rotation
            node = node.parent
        return rotation

    @global_rotation.setter
    def global_rotation(self, rotation: float) -> None:
        diff = rotation - self.global_rotation
        self.rotation += diff
