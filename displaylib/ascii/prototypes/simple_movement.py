from __future__ import annotations

from ...template.type_hints import NodeType
from ..prefabs.sprite import AsciiSprite
from ...math import Vec2
import keyboard


class SimpleMovement2D: # Component (mixin class)
    def __new__(cls: type[NodeType], *args, texture: list[list[str]] = [], offset: Vec2 = Vec2(0, 0), centered = None, z_index: int = 0, force_sort: bool = True, **kwargs) -> NodeType:
        instance = super().__new__(cls, *args, **kwargs) # type: AsciiSprite  # type: ignore
        instance._update = instance._simple_movement_2d_update_wrapper(instance._update) # type: ignore
        return instance # type: ignore
    
    def _simple_movement_2d_update_wrapper(self: AsciiSprite, update_function): # type: ignore
        def update(delta):
            update_function(delta)
            if keyboard.is_pressed("D"):
                self.position.x += 1
            if keyboard.is_pressed("A"):
                self.position.x -= 1
            if keyboard.is_pressed("W"):
                self.position.y -= 1
            if keyboard.is_pressed("S"):
                self.position.y += 1
        return update
