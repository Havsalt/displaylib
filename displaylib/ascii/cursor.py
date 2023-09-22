from __future__ import annotations as _annotations


def set_visibility(visible: bool) -> None:
    raise NotImplemented

def show() -> None:
    set_visibility(True)

def hide() -> None:
    set_visibility(False)

def set_position(x: int, y: int) -> None:
    raise NotImplemented

def set_console_handle(console_handle: int) -> None:
    raise NotImplemented


import os as _os

if _os.name == "nt":  # Windows
    import ctypes as _ctypes

    _console_handle = _ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

    class _CursorInfo(_ctypes.Structure):
        _fields_ = [("size", _ctypes.c_int), ("visible", _ctypes.c_byte)]

    def set_visibility(visible: bool) -> None:
        ci = _CursorInfo()
        _ctypes.windll.kernel32.GetConsoleCursorInfo(_console_handle, _ctypes.byref(ci))
        ci.visible = visible
        _ctypes.windll.kernel32.SetConsoleCursorInfo(_console_handle, _ctypes.byref(ci))

    def set_position(x: int, y: int) -> None:
        value = x + (y << 16)
        _ctypes.windll.kernel32.SetConsoleCursorPosition(_console_handle, value)
    
    def set_console_handle(console_handle: int) -> None:
        global _console_handle
        _console_handle = _ctypes.windll.kernel32.GetStdHandle(console_handle)


else:  # Linux and macOS
    def set_visibility(visible: bool) -> None:
        print("\x1b[?25h" if visible else "\x1b[?25l")

    def clear_screen() -> None:
        print("\x1b[2J\x1b[H")

    def set_position(x: int, y: int) -> None:
        print(end=f"\033[{x};{y}f")


import atexit as _atexit
_atexit.register(hide)
