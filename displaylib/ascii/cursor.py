from __future__ import annotations as _annotations

from ..math import Vec2i

# TODO: implement
# https://stackoverflow.com/questions/880530/can-modules-have-properties-the-same-way-that-objects-can

# NOTE: many of the implementations in this file is sub-optimal

def set_visibility(visible: bool, /) -> None:
    return

def is_visible() -> bool:
    return False

def show() -> None:
    set_visibility(True)

def hide() -> None:
    set_visibility(False)

def get_position() -> Vec2i:
    return Vec2i(0, 0)

def set_position(position: Vec2i, /) -> None:
    return

def get_raw_position(*, font_size: Vec2i = Vec2i(8, 12)) -> Vec2i:
    return Vec2i(0, 0)

def set_raw_position(position: Vec2i, /, *, font_size: Vec2i = Vec2i(8, 12)) -> None:
    return

def set_console_handle(console_handle: int, /) -> None:
    return


import os as _os

if _os.name == "nt":  # Windows
    import ctypes as _ctypes
    import ctypes.wintypes as _wintypes

    _console_handle: int = _ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

    class _CursorInfo(_ctypes.Structure):
        _fields_ = [("size", _ctypes.c_int), ("visible", _ctypes.c_byte)]

    def set_visibility(visible: bool, /) -> None:
        ci = _CursorInfo()
        _ctypes.windll.kernel32.GetConsoleCursorInfo(_console_handle, _ctypes.byref(ci))
        ci.visible = visible
        _ctypes.windll.kernel32.SetConsoleCursorInfo(_console_handle, _ctypes.byref(ci))
    
    def is_visible() -> bool:
        ci = _CursorInfo()
        _ctypes.windll.kernel32.GetConsoleCursorInfo(_console_handle, _ctypes.byref(ci))
        return bool(ci.visible)
    
    class _CONSOLE_SCREEN_BUFFER_INFO(_ctypes.Structure):
        _fields_ = [("dwSize", _wintypes._COORD),
                    ("dwCursorPosition", _wintypes._COORD),
                    ("wAttributes", _wintypes.WORD),
                    ("srWindow", _wintypes.SMALL_RECT),
                    ("dwMaximumWindowSize", _wintypes._COORD)]

    def get_position() -> Vec2i:
        csbi = _CONSOLE_SCREEN_BUFFER_INFO()
        _ctypes.windll.kernel32.GetConsoleScreenBufferInfo(_console_handle, _ctypes.byref(csbi))
        return Vec2i(csbi.dwCursorPosition.X, csbi.dwCursorPosition.Y)

    def set_position(position: Vec2i, /) -> None:
        value = position.x + (position.y << 16)
        _ctypes.windll.kernel32.SetConsoleCursorPosition(_console_handle, value)

    try:
        import win32gui as _win32gui

        def get_raw_position(*, font_size: Vec2i = Vec2i(8, 12)) -> Vec2i:
            raw_point = _wintypes.POINT()
            _ctypes.windll.user32.GetCursorPos(_ctypes.byref(raw_point))
            true_console_handle = _win32gui.GetForegroundWindow()
            (left, top, _, _) = _win32gui.GetWindowRect(true_console_handle)
            relative_x = raw_point.x - left
            relative_y = raw_point.y - top
            return Vec2i(relative_x // font_size.x, relative_y // font_size.y)
    
    except ModuleNotFoundError:
        def get_raw_position(*, font_size: Vec2i = Vec2i(8, 12)) -> Vec2i:
            point = _wintypes.POINT()
            _ctypes.windll.user32.GetCursorPos(_ctypes.byref(point))
            return Vec2i(point.x // font_size.x, point.y // font_size.y)

    def set_raw_position(position: Vec2i, /, *, font_size: Vec2i = Vec2i(8, 12)) -> None:
        _ctypes.windll.user32.SetCursorPos(position.x * font_size.x, position.y * font_size.y)
    
    def set_console_handle(console_handle: int, /) -> None:
        global _console_handle
        _console_handle = _ctypes.windll.kernel32.GetStdHandle(console_handle)


else:  # Linux and macOS (and Windows)
    def set_visibility(visible: bool, /) -> None:
        print(end="\x1b[?25h" if visible else "\x1b[?25l")

    def clear_screen() -> None:
        print(end="\x1b[2J\x1b[H")

    def set_position(position: Vec2i, /) -> None:
        print(end=f"\033[{position.x};{position.y}f")


import atexit as _atexit
_atexit.register(show)
