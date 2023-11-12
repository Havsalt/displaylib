from __future__ import annotations as _annotations

import os as _os
_os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
_os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
from typing import TYPE_CHECKING as _TYPE_CHECKING

import pygame as _pygame
from pygame.constants import JOYDEVICEADDED as _JOYDEVICEADDED, JOYDEVICEREMOVED as _JOYDEVICEREMOVED
if not _pygame.display.get_init():
    _pygame.display.init()
if not _pygame.joystick.get_init():
    _pygame.joystick.init()

if _TYPE_CHECKING:
    from typing import Protocol as _Protocol, Callable as _Callable, Any as _Any
    from ...template.type_hints import EngineType as _EngineType, NodeMixin as _NodeMixin
    from pygame.event import Event as _Event
    from pygame.joystick import JoystickType as _JoystickType

    class _AnyControllerHandlerNode(_NodeMixin, _Protocol):
        joystick: _JoystickType
        has_active_joystick: bool
        def _on_connected(self) -> None: ...
        def _on_disconnected(self) -> None: ...
        def _on_reconnected(self) -> None: ...


class UsingControllerManager: # inject into App/Engine
    _input: _Callable[[_Event], _Any]
    _living_handlers: list[_AnyControllerHandlerNode] = []
    controller_handler: type[_AnyControllerHandlerNode] | None = None

    def __new__(cls: _EngineType, *args, **kwargs) -> _EngineType:
        instance = super().__new__(cls, *args, **kwargs) # type: ignore
        instance._input = instance._using_controller_manager_input_wrapper(instance._input)
        for event in _pygame.event.get():
            # print("INITIAL EVENT:", event)
            if event.type == _JOYDEVICEADDED:
                instance._add_controller_handler(event.device_index)
            elif event.type == _JOYDEVICEREMOVED: # just in case - should be fine
                instance._remove_controller_handler(event.device_index)
        return instance
    
    def _add_controller_handler(self, device_index: int) -> None:
        # print("DEVICE INDEX:", device_index)
        for handler in self._living_handlers:
            if handler.joystick.get_init() == False:
                # print("FOUND HANLDER:", handler.uid)
                new_joystick = _pygame.joystick.Joystick(device_index)
                # print("(REUSING HANDLER) NEW GUID:", new_joystick.get_guid())
                handler.joystick = new_joystick
                handler.has_active_joystick = True
                handler._on_reconnected()
                return
        if self.controller_handler is None:
            raise TypeError(f"class variable 'controller_handler' cannot be of type 'None' when instantiated")
        new_handler = self.controller_handler()
        if not isinstance(new_handler, ControllerClient):
            raise TypeError(f"handler for new controller requires component 'ControllerClient' (use {ControllerClient})")
        # print("MADE HANDLER:", new_handler.uid)
        new_joystick = _pygame.joystick.Joystick(device_index)
        # print("NEW GUID:", new_joystick.get_guid())
        new_handler.joystick = new_joystick
        new_handler.has_active_joystick = True
        new_handler._on_connected()
        self._living_handlers.append(new_handler)
    
    def _remove_controller_handler(self, instance_id: int) -> None:
        for handler in self._living_handlers:
            if handler.joystick.get_init() and handler.joystick.get_instance_id() == instance_id:
                # print("REMOVE WITH INSTANCE ID:", handler.joystick.get_instance_id())
                # put newly disabled handler at beginning of list
                self._living_handlers.remove(handler)
                self._living_handlers.insert(0, handler)
                # disable and activate callback
                handler.has_active_joystick = False
                handler.joystick.quit()
                handler._on_disconnected()
                return
    
    def _using_controller_manager_input_wrapper(self, input_function: _Callable[[_Event], _Any]) -> _Callable[[_Event], _Any]:
        def _input(event: _Event):
            if event.type == _JOYDEVICEADDED:
                # print("ADD:", event)
                self._add_controller_handler(event.device_index)
            elif event.type == _JOYDEVICEREMOVED:
                # print("REMOVE:", event)
                self._remove_controller_handler(event.instance_id)
            input_function(event)
        return _input


class ControllerClient:
    joystick: _JoystickType
    has_active_joystick: bool = False

    def _on_connected(self) -> None:
        ...
    
    def _on_disconnected(self) -> None:
        ...
    
    def _on_reconnected(self) -> None:
        ...
