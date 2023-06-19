from __future__ import annotations


class Color:
    def __init__(self, *, color_code: int | str = 0, fg: bool = True, bg: bool = False) -> None:
        self.color = f"\u001b[38;5;{color_code}m"


class HexColor(Color):
    def __init__(self, *, hex_color: str = "ffffff", fg: bool = True, bg: bool = False) -> None:
        hex_color = hex_color.lower()
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])
        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)

        # convert RGB values to ANSI 256-color code
        color_code = 16 + (red * 36) + (green * 6) + blue
        self.color = f"\u001b[38;5;{color_code}m"
