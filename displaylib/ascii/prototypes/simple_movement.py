from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from ...template.type_hints import NodeType as _NodeType
from .. import keyboard as _keyboard

if _TYPE_CHECKING:
    from typing import Protocol as _Protocol
    from ...template.type_hints import UpdateFunction as _UpdateFunction, ValidTransform2DNode as _ValidTransform2DNode
    
    class _ValidSimpleMovement2DNode(_ValidTransform2DNode, _Protocol):
        def _simple_movement_2d_update_wrapper(self: _ValidSimpleMovement2DNode, update_function: _UpdateFunction) -> _UpdateFunction:
            ...


class SimpleMovement2D: # Component (mixin class)
    def __new__(cls: type[_NodeType], *args, **kwargs) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs) # type: _ValidSimpleMovement2DNode  # type: ignore
        instance._update = instance._simple_movement_2d_update_wrapper(instance._update) # type: ignore
        return instance # type: ignore
    
    def _simple_movement_2d_update_wrapper(self: _ValidSimpleMovement2DNode, update_function: _UpdateFunction) -> _UpdateFunction:
        def _update(delta: float):
            if _keyboard.is_pressed("D"):
                self.position.x += 1
            if _keyboard.is_pressed("A"):
                self.position.x -= 1
            if _keyboard.is_pressed("W"):
                self.position.y -= 1
            if _keyboard.is_pressed("S"):
                self.position.y += 1
            update_function(delta)
        return _update
