from __future__ import annotations as _annotations


def is_pressed(hotkey: _Key | _ScanCodeList) -> bool:
    # TODO: make implementation
    return False

try:
    import keyboard as _keyboard
    from typing import TypeAlias as _TypeAlias

    _Key: _TypeAlias = int | str
    _ScanCodeList: _TypeAlias = list[int] | tuple[int, ...]

    def is_pressed(hotkey: _Key | _ScanCodeList) -> bool:
        return _keyboard.is_pressed(hotkey)

except ModuleNotFoundError:
    pass
