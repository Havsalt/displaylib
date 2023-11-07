from __future__ import annotations

import copy
from functools import partial
from typing import TYPE_CHECKING, TypeVar, ClassVar, Protocol, Callable, Any, cast

import keyboard
from ...template import Transform2D
from ...template.type_hints import MroNext, NodeType, NodeMixin, UpdateFunction
from .. import Node, Texture
from ..type_hints import TextureMixin
from ..prototypes.controller_support import ControllerSupport

if TYPE_CHECKING:
    FocusSelf = TypeVar("FocusSelf", bound="Focus")

class FocusMixin(Protocol):
    @property
    def texture_focused(self) -> list[list[str]]: ...
    @texture_focused.setter
    def texture_focused(self, value: list[list[str]]) -> None: ...
    @property
    def _texture_unfocused(self) -> list[list[str]]: ...
    @_texture_unfocused.setter
    def _texture_unfocused(self, value: list[list[str]]) -> None: ...
    def grab_focus(self) -> None: ...
    @property
    def _focus_update_wrapper(self) -> Callable[..., Any]: ...
    @_focus_update_wrapper.setter
    def _focus_update_wrapper(self, value: Callable[..., Any]) -> None: ...

class ValidFocusNode(FocusMixin, TextureMixin, NodeMixin, Protocol):
    def __new__(cls, *args, **kwargs) -> ValidFocusNode: ...


# controller bindings
def _is_next_focused(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    return self.joystick.get_button(14)
def _is_right_focused(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    return self.joystick.get_button(14)
def _is_previous_focused(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    return self.joystick.get_button(13)
def _is_left_focused(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    return self.joystick.get_button(13)
def _is_top_focused(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    return self.joystick.get_button(11)
def _is_bottom_focused(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    return self.joystick.get_button(12)
def _is_trigger_pressed(self: ControllerSupport) -> bool:
    assert self.joystick is not None
    return self.joystick.get_button(0)

class Focus(ControllerSupport): # Component (mixin class)
    """`Focus` component
    """
    bindings = [
        _is_next_focused,
        _is_previous_focused,
        _is_left_focused,
        _is_right_focused,
        _is_top_focused,
        _is_bottom_focused,
        _is_trigger_pressed
    ]
    current: ClassVar[ValidFocusNode]
    _focus_default: ClassVar[ValidFocusNode]
    texture_focused: list[list[str]]
    disabled = False
    element_next: ValidFocusNode | None = None
    element_previous: ValidFocusNode | None = None
    element_left: ValidFocusNode | None = None
    element_right: ValidFocusNode | None = None
    element_top: ValidFocusNode | None = None
    element_bottom: ValidFocusNode | None = None
    _texture_unfocused: list[list[str]]
    _key_released: bool = True
    _transition_pressed: bool = False
    _performed_focus_ownership_transition: bool = False
    
    def __new__(cls: type[NodeType], *args, texture: list[list[str]] = [], **kwargs) -> NodeType:
        mro_next = cast(MroNext[ValidFocusNode], super())
        instance = mro_next.__new__(cls, *args, texture=texture, **kwargs)
        # override -> class value -> default @ proxy _texture_unfocused << texture
        if texture or not hasattr(instance, "texture"):
            instance._texture_unfocused = texture
        else:
            instance._texture_unfocused = instance.texture
        # class value -> default
        if not hasattr(instance, "texture_focused"):
            instance.texture_focused = instance.texture
        # apply update wrapper
        instance._update = instance._focus_update_wrapper(instance._update)
        return cast(NodeType, instance)

    def make_unique(self) -> None:
        """Makes a deepcopy of `.texture`, which is then set as the new texture
        """
        self._texture_unfocused = copy.deepcopy(self._texture_unfocused)
        cast(TextureMixin, super()).make_unique()
    
    @staticmethod
    def get_focused() -> ValidFocusNode:
        return Focus.current

    def grab_focus(self) -> None:
        Focus.current.texture = Focus.current._texture_unfocused
        self = cast(ValidFocusNode, self)
        Focus.current = self
        self.texture = self.texture_focused
    
    def with_focus_grabbed(self: FocusSelf) -> FocusSelf:
        self.grab_focus()
        return self
    
    def has_focus(self) -> bool:
        return Focus.current is self

    def release_focus(self):
        self.texture = self._texture_unfocused
        Focus.current = Focus._focus_default

    def _is_next_focused(self) -> bool:
        return keyboard.is_pressed(15)

    def _is_previous_focused(self) -> bool:
        return keyboard.is_pressed([42, 15])

    def _is_left_focused(self) -> bool:
        return keyboard.is_pressed(75)

    def _is_right_focused(self) -> bool:
        return keyboard.is_pressed(77)
    
    def _is_top_focused(self) -> bool:
        return keyboard.is_pressed(72)

    def _is_bottom_focused(self) -> bool:
        return keyboard.is_pressed(80)

    def _is_trigger_pressed(self) -> bool:
        return keyboard.is_pressed("space")
    
    def _focus_update_wrapper(self, update: UpdateFunction) -> UpdateFunction:
        def _update(delta: float):
            if not self.disabled:
                if Focus._transition_pressed:
                    if not any((self._is_next_focused(),
                            self._is_previous_focused(),
                            self._is_left_focused(),
                            self._is_right_focused(),
                            self._is_top_focused(),
                            self._is_bottom_focused())):
                        Focus._transition_pressed = False
                elif not Focus._performed_focus_ownership_transition and self.has_focus():
                    if self.element_previous is not None and self._is_previous_focused():
                        self.release_focus()
                        self.element_previous.grab_focus()
                        Focus._transition_pressed = True
                        Focus._performed_focus_ownership_transition = True
                    elif self.element_next is not None and self._is_next_focused():
                        self.release_focus()
                        self.element_next.grab_focus()
                        Focus._transition_pressed = True
                        Focus._performed_focus_ownership_transition = True
                    elif self.element_left is not None and self._is_left_focused():
                        self.release_focus()
                        self.element_left.grab_focus()
                        Focus._transition_pressed = True
                        Focus._performed_focus_ownership_transition = True
                    elif self.element_right is not None and self._is_right_focused():
                        self.release_focus()
                        self.element_right.grab_focus()
                        Focus._transition_pressed = True
                        Focus._performed_focus_ownership_transition = True
                    elif self.element_next is not None and self.element_right is None and self._is_right_focused():
                        self.release_focus()
                        self.element_next.grab_focus()
                        Focus._transition_pressed = True
                        Focus._performed_focus_ownership_transition = True
                    elif self.element_previous is not None and self.element_left is None and self._is_left_focused():
                        self.release_focus()
                        self.element_previous.grab_focus()
                        Focus._transition_pressed = True
                        Focus._performed_focus_ownership_transition = True
                    elif self.element_top is not None and self._is_top_focused():
                        self.release_focus()
                        self.element_top.grab_focus()
                        Focus._transition_pressed = True
                        Focus._performed_focus_ownership_transition = True
                    elif self.element_bottom is not None and self._is_bottom_focused():
                        self.release_focus()
                        self.element_bottom.grab_focus()
                        Focus._transition_pressed = True
                        Focus._performed_focus_ownership_transition = True
            update(delta)
        return _update


class DefaultFocusNode(Focus, Texture, Transform2D, Node):
    def queue_free(self) -> None:
        # singleton instance should not be deleted as is is used as default
        # NOTE: do not remove from Node.nodes
        return

Focus._focus_default = DefaultFocusNode()
Focus.current = DefaultFocusNode._focus_default
