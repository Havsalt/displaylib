from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

if TYPE_CHECKING:
    from .engine import Engine

Self = TypeVar("Self")


class NodeMixinSortMeta(type):
    """Node metaclass for initializing `Node` subclass after other `mixin` classes
    """
    @staticmethod
    def _mixin_sort(base: type) -> bool:
        return issubclass(base, Node)

    def __new__(cls, name: str, bases: tuple[type], attrs: dict[str, object]):
        sorted_bases = tuple(sorted(bases, key=NodeMixinSortMeta._mixin_sort))
        return super().__new__(cls, name, sorted_bases, attrs)


class Node(metaclass=NodeMixinSortMeta):
    """`Node` base class

    Automatically keeps track of alive Node(s) by reference.
    An Engine subclass may access it's nodes through the `nodes` class attribute

    Hooks:
        - `_update(self, delta: float) -> None`
    """
    root: Engine # set from a Engine subclass
    nodes: ClassVar[dict[str, Node]] = {} # all nodes that are alive
    _uid_counter: ClassVar[int] = 0 # is read and increments for each generated uid
    _request_process_priority_sort: ClassVar[bool] = False # requests Engine to sort
    _queued_nodes: list[str] = [] # uses <Node>.queue_free() to ask Engine to delete a node based on UID
    # instance spesific
    uid: str
    parent: Node | None

    def __new__(cls: type[Self], *parent: Node | None, force_sort: bool = True) -> Self: # pulling: optional "parent", "force_sort"
        """In addition to default behaviour, automatically stores the node in a dict.
        Keeps the object alive by the reference stored

        Args:
            cls (type[Node]): class of the node being created

        Returns:
            Node: node instance that was stored
        """
        if len(parent) > 1: # if passing anything more than `parent` as positional argument
            raise ValueError(f"expected 0-1 argument for 'parent', was given {len(parent)}: {parent}")
        instance = super().__new__(cls)
        uid = cls.generate_uid()
        instance.uid = uid
        Node.nodes[uid] = instance
        return instance

    @classmethod
    def generate_uid(cls) -> str:
        """Generates a unique ID by incrementing an internal counter

        Returns:
            str: unique ID
        """
        uid = Node._uid_counter
        Node._uid_counter += 1
        return str(uid)

    def __init__(self, parent: Node | None = None, *, force_sort: bool = True) -> None:
        self.parent = parent
        self._process_priority = 0
        if force_sort: # may sort `process_priority` and `z_index`
            Node._request_process_priority_sort = True # otherwise, depent on a `process_priority` change

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

    @property
    def process_priority(self) -> int:
        return self._process_priority

    @process_priority.setter
    def process_priority(self, value: int) -> None:
        if self._process_priority != value: # if changed
            self._process_priority = value
            Node._request_process_priority_sort = True

    def where(self: Self, **attributes) -> Self:
        """Sets/overrides the given attributes of the node instance

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
        """Tells the Engine to `delete` this node after
        every node has been called `_update` on
        """
        if not self.uid in Node._queued_nodes:
            Node._queued_nodes.append(self.uid)
        Node._request_process_priority_sort = True
