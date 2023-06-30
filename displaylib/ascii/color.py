from __future__ import annotations

from typing import TypeAlias

ColorCode: TypeAlias = int | str
OptionalColorCode: TypeAlias = int | str | None
HexCode: TypeAlias = str
OptionalHexCode: TypeAlias = str | None


class Color:
    def __init__(self, fg: ColorCode = 7, bg: OptionalColorCode = None) -> None:
        self.value = f"\u001b[38;5;{fg}m"
        if bg is not None:
            self.value += f"\u001b[48;5;{bg}m"


class HexColor(Color):
    def __init__(self, fg: HexCode = "ffffff", bg: OptionalHexCode = None) -> None:
        fg = fg.lower()
        if len(fg) == 3:
            fg = "".join([c * 2 for c in fg])
        red = int(fg[0:2], 16)
        green = int(fg[2:4], 16)
        blue = int(fg[4:6], 16)
        # convert RGB values to ANSI 256-color code
        fg_code = 16 + (red * 36) + (green * 6) + blue
        self.value = f"m\u001b[38;5;{fg_code}m"

        if bg is None:
            return # do not compute background color
    
        bg = bg.lower()
        if len(bg) == 3:
            bg = "".join([c * 2 for c in bg])
        red = int(bg[0:2], 16)
        green = int(bg[2:4], 16)
        blue = int(bg[4:6], 16)
        # convert RGB values to ANSI 256-color code
        bg_code = 16 + (red * 36) + (green * 6) + blue
        self.value += f"\u001b[48;5;{bg_code}m"
