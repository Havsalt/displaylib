from __future__ import annotations

# NOTE: this prototype requires `pygame` and `keyboard` to be installed

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
import math
from functools import partial
from typing import TYPE_CHECKING, ClassVar, Protocol, Callable, Any, cast

from ...math import Vec2
from ...template.type_hints import MroNext, NodeType

import keyboard
import pygame
if not pygame.display.get_init():
    pygame.display.init()
if not pygame.joystick.get_init():
    pygame.joystick.init()

if TYPE_CHECKING:
    from pygame.joystick import JoystickType

class ControllerProtocol(Protocol):
    @property
    def treshold(self) -> float: ...
    @treshold.setter
    def treshold(self, value: float) -> None: ...
    @property
    def _controller_support_update_wrapper(self) -> Callable[[function], function]: ...
    @_controller_support_update_wrapper.setter
    def _controller_support_update_wrapper(self, value: Callable[[function], function]) -> None: ...
    @property
    def _update(self) -> function: ...
    @_update.setter
    def _update(self, value: function) -> None: ...
    @property
    def bindings(self) -> list[Callable[..., Any]]: ...
    @property
    def joystick(self) -> JoystickType | None: ...
    @joystick.setter
    def joystick(self, value: JoystickType | None) -> None: ...


class ControllerSupport: # Component (mixin class)
    bindings: ClassVar[list[Callable[..., Any]]] = []
    treshold: float = 0.3
    joystick: JoystickType | None

    def __new__(cls: type[NodeType], *args, device_index: int = 0, **kwargs) -> NodeType:
        if device_index is None:
            return super().__new__(cls, *args, **kwargs)
        mro_next = cast(MroNext[ControllerProtocol], super())
        instance = mro_next.__new__(cls, *args, **kwargs)
        try:
            instance.joystick = pygame.joystick.Joystick(device_index)
        except pygame.error:
            instance.joystick = None
            return cast(NodeType, instance)
        instance._update = instance._controller_support_update_wrapper(instance._update)
        for function in instance.bindings:
            setattr(instance, function.__name__, partial(function, instance))
        return cast(NodeType, instance)

    @staticmethod
    def _controller_support_update_wrapper(update) -> function:
        def _update(delta: float) -> None:
            pygame.event.pump()
            update(delta)
        return _update


# keyboard movement
class SimpleMovement: # Component (mixin class)
    speed = 1
    position: Vec2

    def is_moving_left(self) -> bool:
        return keyboard.is_pressed("a")
    
    def is_moving_right(self) -> bool:
        return keyboard.is_pressed("d")
    
    def is_moving_up(self) -> bool:
        return keyboard.is_pressed("w")

    def is_moving_down(self) -> bool:
        return keyboard.is_pressed("s")

    def get_movement_direction(self) -> Vec2:
        return Vec2(int(self.is_moving_right()) - int(self.is_moving_left()),
                    int(self.is_moving_down()) - int(self.is_moving_up())
                    ).normalized()

    def get_movement_direction_strength(self) -> Vec2:
        return Vec2(int(self.is_moving_right()) - int(self.is_moving_left()),
                    int(self.is_moving_down()) - int(self.is_moving_up()))

    def _update(self, delta: float) -> None:
        self.position += self.get_movement_direction() * self.speed


# controller bindings
TRESHOLD = 0.3

def is_moving_left(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    raw = Vec2(self.joystick.get_axis(0), self.joystick.get_axis(1))
    if raw.length() < TRESHOLD:
        return False
    direction = raw.normalized()
    rotated = direction.rotated(math.radians(45)) # 45 deg
    if rotated.x < 0:
        if rotated.y > 0:
            return True
    return False

def is_moving_right(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    raw = Vec2(self.joystick.get_axis(0), self.joystick.get_axis(1))
    if raw.length() < TRESHOLD:
        return False
    direction = raw.normalized()
    rotated = direction.rotated(math.radians(45)) # 45 deg
    if rotated.x > 0:
        if rotated.y < 0:
            return True
    return False

def is_moving_up(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    raw = Vec2(self.joystick.get_axis(0), self.joystick.get_axis(1))
    if raw.length() < TRESHOLD:
        return False
    direction = raw.normalized()
    rotated = direction.rotated(math.radians(45)) # 45 deg
    if rotated.x < 0:
        if rotated.y < 0:
            return True
    return False

def is_moving_down(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    raw = Vec2(self.joystick.get_axis(0), self.joystick.get_axis(1))
    if raw.length() < TRESHOLD:
        return False
    direction = raw.normalized()
    rotated = direction.rotated(math.radians(45)) # 45 deg
    if rotated.x > 0:
        if rotated.y > 0:
            return True
    return False

def get_movement_direction_strength(self: ControllerSupport) -> Vec2:
    assert self.joystick is not None
    return Vec2(self.joystick.get_axis(0), self.joystick.get_axis(1))


class SimpleControllerSupportedMovement(ControllerSupport, SimpleMovement): # Extended Component (mixin class)
    bindings = [
        is_moving_left,
        is_moving_right,
        is_moving_up,
        is_moving_down,
        get_movement_direction_strength
    ]
