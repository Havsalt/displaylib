from __future__ import annotations as _annotations

import os as _os
_os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from typing import TYPE_CHECKING as _TYPE_CHECKING, Any as _Any

from ...math import Vec2 as _Vec2

from pygame.constants import K_w as _K_w, K_a as _K_a, K_s as _K_s, K_d as _K_d
from pygame import key as _key

if _TYPE_CHECKING:
    from typing import Protocol as _Protocol
    from ...template.type_hints import NodeType as _NodeType, ValidTransform2DNode as _ValidTransform2DNode, UpdateFunction as _UpdateFunction
    
    class _ValidSimpleMovement2DNode(_ValidTransform2DNode, _Protocol):
        speed_modifier: _Vec2
        normalize_direction: bool
        def _simple_movement_2d_update_wrapper(self: _ValidSimpleMovement2DNode, input_function: function) -> function:
            ...


class SimpleMovement2D: # Component (mixin class)
    speed_modifier: _Vec2
    normalize_direction: bool = True # whether to normalize the direction vector

    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs) # type: ignore
        instance._update = instance._simple_movement_2d_update_wrapper(instance._update) # type: ignore
        # class value -> 'default
        if not hasattr(instance, "speed_modifier"):
            instance.speed_modifier = _Vec2(1, 1)
        return instance
    
    def _simple_movement_2d_update_wrapper(self: _ValidSimpleMovement2DNode, update_function: _UpdateFunction) -> _UpdateFunction:
        def _update(delta: float):
            keys = _key.get_pressed()
            direction = _Vec2.ZERO
            if keys[_K_d]:
                direction.x += 1
            if keys[_K_a]:
                direction.x -= 1
            if keys[_K_w]:
                direction.y -= 1
            if keys[_K_s]:
                direction.y += 1
            if self.normalize_direction:
                direction = direction.normalized()
            self.position += direction * self.speed_modifier
            update_function(delta)
        return _update
