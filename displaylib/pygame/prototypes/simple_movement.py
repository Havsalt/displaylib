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
    from pygame.joystick import JoystickType as _JoystickType

    class _ValidSimpleMovement2DNode(_ValidTransform2DNode, _Protocol):
        normalize_direction: bool
        speed_modifier: _Vec2
        def _simple_movement_2d_update_wrapper(self: _ValidSimpleMovement2DNode, input_function: function) -> function: ...
    
    class _ValidSimpleControllerMovement2DNode(_ValidTransform2DNode, _Protocol):
        normalize_direction: bool
        speed_modifier: _Vec2
        snap_direction: bool
        dead_zone_threshold: _Vec2
        joystick: _JoystickType
        def _simple_movement_2d_update_wrapper(self: _ValidSimpleMovement2DNode, input_function: function) -> function: ...


class SimpleMovement2D: # Component (mixin class)
    normalize_direction: bool = True # whether to normalize the direction vector
    speed_modifier: _Vec2

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


class SimpleControllerMovement2D: # Component (mixin class)
    normalize_direction: bool = True # whether to normalize the direction vector
    speed_modifier: _Vec2 = _Vec2(1, 1)
    snap_direction: bool = False
    dead_zone_threshold: _Vec2 = _Vec2(0.1, 0.1)
    joystick: _JoystickType

    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs) # type: ignore
        instance._update = instance._simple_controller_movement_2d_update_wrapper(instance._update) # type: ignore
        # class value -> 'default
        if not hasattr(instance, "speed_modifier"):
            instance.speed_modifier = _Vec2(1, 1)
        else:
            instance.speed_modifier = instance.speed_modifier.copy()
        # class value -> 'default
        if not hasattr(instance, "dead_zone_threshold"):
            instance.dead_zone_threshold = _Vec2(0.1, 0.1)
        else:
            instance.dead_zone_threshold = instance.dead_zone_threshold.copy()
        return instance
    
    def _simple_controller_movement_2d_update_wrapper(self: _ValidSimpleControllerMovement2DNode, update_function: _UpdateFunction) -> _UpdateFunction:
        def _update(delta: float):
            if self.joystick.get_init():
                direction = _Vec2(
                    self.joystick.get_axis(0),
                    self.joystick.get_axis(1)
                ).clamped(-(_Vec2.ONE), (_Vec2.ONE))
                if abs(direction.x) < self.dead_zone_threshold.x:
                    direction.x = 0
                if abs(direction.y) < self.dead_zone_threshold.y:
                    direction.y = 0
                strength = abs(direction.copy())
                if self.normalize_direction:
                    direction = direction.normalized()
                if not self.snap_direction and direction:
                    direction = direction * strength
                    # FIXME: diagonal movement should be longer
                self.position += direction * self.speed_modifier
            update_function(delta)
        return _update
