from typing_extensions import Self
from typing import TYPE_CHECKING
from ..math import Vec2


if TYPE_CHECKING:
    from .engine import Engine


class Node:
    """Node base class

    Automatically keeps track of alive Node(s) by reference.
    An Engine subclass may access it's nodes through the `nodes` class attribute
    """
    __logical__: bool = True # logical means it won't have a position or existance in the "real world"

    root: "Engine" = None # set from a Engine subclass
    nodes: dict[int, Self] = {} # all nodes that are alive
    _request_sort: bool = False # requests Engine to sort
    _queued_nodes: set = set() # uses <Node>.queue_free() to ask Engine to delete them

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        instance = super().__new__(cls)
        Node.nodes[id(instance)] = instance
        return instance

    def __init__(self, parent: Self | None = None, *, force_sort: bool = True) -> None:
        self.parent = parent
        self.z_index = 0 # static
        if force_sort: # if True, requests sort every frame a new node is created
            Node._request_sort = True # otherwise, depent on a `z_index` change

    def __repr__(self) -> str:
        """Returns a default representation of the Node object

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

    def where(self, **attributes) -> Self:
        for key, value in attributes.items():
            setattr(self, key, value)
        return self

    def _update(self, delta: float) -> None:
        """Called every frame by the Engine class
        
        Override for custom functionality

        Args:
            delta (float): time since last frame
        """
        return
    
    def queue_free(self) -> None:
        """Tells the Engine to `delete` this <Node> after
        every node has been called `_update` on
        """
        Node._queued_nodes.add(self)


class Node2D(Node):
    """Node2D class with transform attributes
    """
    __logical__: bool = False

    def __init__(self, parent: Self | None = None, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        self.parent = parent
        self.position = Vec2(x, y)
        self._z_index = z_index
        self.visible = True # only nodes on the 2D plane will have the option to be visible
        if force_sort: # if True, requests sort every frame a new node is created
            Node._request_sort = True # otherwise, depend on a `z_index` change
    
    def __repr__(self) -> str:
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
        position = self.position
        node = self.parent
        while node != None:
            position += node.position
            node = node.parent
        return position
    
    @global_position.setter
    def global_position(self, position: Vec2) -> None:
        diff = position - self.global_position
        self.position += diff
