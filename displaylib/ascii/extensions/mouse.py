from __future__ import annotations

import ctypes # TODO: add system spesific implementations for Linux and macOS
from ctypes import wintypes

from ..math import Vec2i
from .camera import AsciiCamera
from .prefab.sprite import AsciiSprite


class MouseEvent:
    __slots__ = tuple()
    def __str__(self) -> str:
        return f"{__class__.__name__}({', '.join(f'{name}={str(getattr(self, name))}' for name in self.__slots__)})"

    def __eq__(self, other: type) -> bool:
        return isinstance(self, other)

class MouseMotionEvent(MouseEvent):
    __slots__ = ("position",)
    def __init__(self, position: Vec2i) -> None:
        self.position = position


def get_mouse_position() -> Vec2i:
    return Vec2i()
#     """Returns the mouse position given in world coordinates

#     Returns:
#         Vec2i: mouse position
#     """
#     # Get the handle of the terminal window
#     hwnd = ctypes.windll.kernel32.GetConsoleWindow()

#     # Get the current cursor position
#     point = wintypes.POINT()
#     ctypes.windll.user32.GetCursorPos(ctypes.byref(point))

#     # Get the window rect
#     rect = wintypes.RECT()
#     ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))

#     # Convert screen coordinates to client coordinates of the terminal window
#     # ctypes.windll.user32.ScreenToClient(hwnd, ctypes.byref(point))

#     return Vec2i((point.x - rect.top) // 12, (point.y - rect.left) // 8)


# def get_mouse_position():
#     # Get handle to the console window
#     kernel32 = ctypes.windll.kernel32
#     console_handle = kernel32.GetConsoleWindow()

#     # Get the current cursor position
#     cursor_position = wintypes.POINT()
#     kernel32.GetConsoleScreenBufferInfo(console_handle, ctypes.byref(cursor_position))
#     return Vec2i(cursor_position.X, cursor_position.Y)


class Cursor(AsciiSprite):
    texture = [["\u001b[31m" + " " + "\u001b[0m"]]

    def _on_mouse_event(self, event: MouseEvent) -> None:
        if isinstance(event, MouseMotionEvent):
            self.global_position = AsciiCamera.current.global_position + event.position
