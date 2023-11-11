from __future__ import annotations as _annotations

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
from typing import TYPE_CHECKING

import pygame
if not pygame.display.get_init():
    pygame.display.init()
if not pygame.joystick.get_init():
    pygame.joystick.init()

if TYPE_CHECKING:
    from ...template.type_hints import EngineType
    from pygame.joystick import JoystickType


class UsingControllerManager: # inject into App/Engine
    _connected_joysticks: list[JoystickType] = []
    
    def __new__(cls: EngineType, *args, **kwargs) -> EngineType:
        instance = super().__new__(cls, *args, **kwargs) # type: ignore
        return instance


class ControllerClient:
    joystick: JoystickType
