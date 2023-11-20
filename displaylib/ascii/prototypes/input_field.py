from __future__ import annotations as _annotations

import string as _string
from typing import TYPE_CHECKING as _TYPE_CHECKING

from displaylib.ascii import color as _color_module
from displaylib.ascii.color import ColorValue as _ColorValue
from displaylib.math import Vec2 as _Vec2
from displaylib.template.type_hints import AnyNode as _AnyNode

from ..prefabs.sprite import AsciiSprite as _AsciiSprite
from ..prefabs.label import AsciiLabel as _AsciiLabel

if _TYPE_CHECKING:
    from types import TracebackType as _TracebackType

try:
    import keyboard as _keyboard
except ModuleNotFoundError as _error:
    raise ModuleNotFoundError("missing external module: keyboard, which is required to use this submodule") from _error


class _InputFieldCaret(_AsciiSprite):
    """A caret for the `InputField`
    """
    color=_color_module.GRAY
    texture=[["_"]]


_ADDITIONAL_SYMBOLS: str = "\"¤%&-_(|)=`?´<!>@£$€{+}\\[/]~^¨*',;#.:"


class InputField(_AsciiLabel):
    """Prefabricated `InputField` that writes what the user types.
    Call `.begin_write()` to start accepting input, and `.end_write()` to stop.
    Can be used with a `context manager`, invoking `.begin_write()` and `.end_write()`.
    This state can also be changed 
    
    Components (inherited from `Label`):
        - `Transform2D`: gives a position and rotation
        - `Texture`: allows the node to be shown
        - `Color`: applies color to the texture
    """
    valid_keys: list[str] = list(_string.ascii_letters + _string.digits + _ADDITIONAL_SYMBOLS)
    key_space: str = "space"
    key_remove: str = "backspace"
    key_confirm: str = "enter"
    key_newline: str | None = None
    scan_code_left: int = 75
    scan_code_right: int = 77
    clear_on_confirm: bool = False
    is_writing: bool = False
    
    def __init__(self, parent: _AnyNode | None = None, *, x: float = 0, y: float = 0, text: str = "", color: _ColorValue = _color_module.WHITE, delimiter: str = "\n", offset: _Vec2 = _Vec2.ZERO, centered: bool = False, z_index: int = 0, force_sort: bool = True) -> None:
        _keyboard.on_press(callback=self._on_key_pressed, suppress=False)
        self._caret_index = len(self.text)
        self.caret = _InputFieldCaret(self)
        self.caret.position = self.get_caret_position()
        self.caret.hide()
    
    def __enter__(self) -> None:
        self.begin_write()
    
    def __exit__(self, _exc_type: type[BaseException] | None, _exc_value: BaseException | None, _exc_tb: _TracebackType | None) -> bool | None:
        self.begin_write()

    def _on_key_pressed(self, key: _keyboard.KeyboardEvent) -> None:
        if not self.is_writing:
            return
        
        if key.name == self.key_space:
            new_chars = list(self.text)
            new_chars.insert(self._caret_index, " ")
            self._caret_index += 1
            self.text = "".join(new_chars)
        
        elif key.name == self.key_remove:
            if self._caret_index > 0:
                new_chars = list(self.text)
                new_chars.pop(self._caret_index -1)
                self._caret_index -= 1
                self.text = "".join(new_chars)
        
        elif key.name == self.key_confirm:
            self.on_confirm(self.text)
            if self.clear_on_confirm:
                self.clear_text()
        
        elif key.name == self.key_newline: # NOTE: this check is made after `.key_confirm`
            new_chars = list(self.text)
            new_chars.insert(self._caret_index, "\n")
            self._caret_index += 1
            self.text = "".join(new_chars)
        
        elif key.name in self.valid_keys:
            new_chars = list(self.text)
            new_chars.insert(self._caret_index, key.name)
            self._caret_index += 1
            self.text = "".join(new_chars)
        
        elif key.scan_code == self.scan_code_left:
            self._caret_index = max(0, self._caret_index - 1)
        
        elif key.scan_code == self.scan_code_right:
            self._caret_index = min(len(self.text), self._caret_index + 1)

        self.caret.position = self.get_caret_position()
    
    def get_caret_position(self) -> _Vec2:
        """Calculates the caret's local position based on input field text content

        Returns:
            Vec2: local caret position
        """
        x, y = 0, 0
        for char in self.text[:self._caret_index]:
            if char == self.delimiter:
                y += 1
                x = 0
            else:
                x += 1
        return _Vec2(x, y)
    
    def clear_text(self) -> None:
        """Clears the text content of the input field
        """
        self.text = ""
    
    def begin_write(self) -> None:
        self.is_writing = True
        self.caret.show()
    
    def end_write(self) -> None:
        self.is_writing = False
        self.caret.hide()
        
    def on_confirm(self, text: str) -> None:
        """Called when the confirm button is pressed.
        By default, clears the text on confirm (normally the 'enter' button)
        
        Override for custom functionality

        Args:
            text (str): text written and confirmed
        """
        ...
