from __future__ import annotations

from typing import TYPE_CHECKING

from ..template import Node, Transform2D

if TYPE_CHECKING:
    import pygame
    from ..template.type_hints import AnyNode
    from .engine import PygameEngine


class Pygame: # mode class with common hooks
    """`Pygame` class that enables common hooks for the `pygame` mode

    Hooks:
        `_input(self, event: pygame.event.Event) -> None`
        `_render(self, surface: pygame.Surface) -> None`
    """
    root: PygameEngine

    def _input(self, event: pygame.event.Event) -> None:
        """Override for custom functionality

        Args:
            event (pygame.event.Event): event received
        """
        ...
    
    def _render(self, surface: pygame.Surface) -> None:
        """Override for custom functionality

        Args:
            surface (pygame.Surface): surface to render custom content onto
        """
        ...


class PygameNode(Pygame, Node): # a variant of the Node
    """`PygameNode` with additional hooks related to `pygame` mode functionality

    Hooks:
        `_input(self, event: pygame.event.Event) -> None`
        `_render(self, surface: pygame.Surface) -> None`
    """


class PygameNode2D(Pygame, Transform2D, Node): # a variant of the Node2D
    """`PygameNode2D` with additional hooks related to `pygame` mode functionality

    Hooks:
        `_input(self, event: pygame.event.Event) -> None`
        `_render(self, surface: pygame.Surface) -> None`
    """
    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, force_sort: bool = True) -> None:
        ...
