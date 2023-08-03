from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, cast

from .type_hints import MroNext, NodeType, AnyNode, Self

if TYPE_CHECKING:
    from ..template.type_hints import AnyNode
    from .engine import Engine


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
    An Engine subclass may access it's nodes through the `.nodes` class attribute

    Hooks:
        - `_update(self, delta: float) -> None`
    """
    nodes: ClassVar[dict[str, AnyNode]] = {} # all nodes that are alive
    _uid_counter: ClassVar[int] = 0 # is read and increments for each generated uid
    _request_process_priority_sort: ClassVar[bool] = False # requests Engine to sort
    _queued_nodes: ClassVar[list[str]] = [] # uses <Node>.queue_free() to ask Engine to delete a node based on UID
    root: Engine # set from a Engine subclass
    uid: str
    parent: AnyNode | None = None

    def __new__(cls: type[NodeType], *parent_as_positional: AnyNode | None, parent: AnyNode | None = None, force_sort: bool = True, **_overflow) -> NodeType:
        """Assigns the node a `unique ID`, stores its `reference` to keep it from being garbage collected and
        may request the engine to `sort` nodes based on '.process_priority'

        Args:
            cls (type[NodeType]): original class that will be created
            parent_as_positional/parent (AnyNode | None, optional): parent of the node. Defaults to None.
            force_sort (bool, optional): whether to request the engine to sort nodes based on '.process_priority'. Defaults to True.

        Raises:
            ValueError: passed more than 1 positional argument, meant to be 'parent' argument
            ValueError: argument 'parent' was passed as both positional and keyword

        Returns:
            NodeType: node instance that was stored
        """
        if len(parent_as_positional) > 1:
            # if passing anything more than `parent` as positional argument
            raise ValueError(f"expected 0-1 argument for 'parent', was given {len(parent_as_positional)}: {parent_as_positional}")
        elif parent is not None and len(parent_as_positional) > 1: # > 1 because it is 'cls' argument
            raise ValueError(f"parameter 'parent' was supplied both positional only and keyword only argument(s): positional(s) = {parent_as_positional} & keyword = {parent_as_positional}")
        mro_next = cast(MroNext[AnyNode], super())
        instance = mro_next.__new__(cls)
        uid = cast(Node, cls).generate_uid()
        instance.uid = uid
        # positional -> keyword/default
        parent_ref = parent_as_positional[0] if parent_as_positional else parent
        instance.parent = parent_ref
        # class value -> default
        instance._process_priority = getattr(instance, "process_priority", 0)
        Node.nodes[uid] = instance # store reference
        if force_sort: # if True, requests sort every frame a new node is created
            Node._request_process_priority_sort = True # otherwise, depend on a `process_priority` change
        return cast(NodeType, instance)

    @classmethod
    def generate_uid(cls) -> str:
        """Generates a unique ID by incrementing an internal counter

        Returns:
            str: unique ID
        """
        uid = Node._uid_counter
        Node._uid_counter += 1
        return str(uid)

    def __init__(self, parent: AnyNode | None = None, *, force_sort: bool = True) -> None:
        """Initializes the base node

        Args:
            parent (AnyNode | None, optional): parent node. Defaults to None.
            force_sort (bool, optional): whether to sort based on 'z_index' and 'process_priority'. Defaults to True.
        """

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
        if self.uid not in Node._queued_nodes:
            Node._queued_nodes.append(self.uid)
        Node._request_process_priority_sort = True
