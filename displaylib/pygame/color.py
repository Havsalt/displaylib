from __future__ import annotations as _annotations

import random as _random
from typing import TypeAlias as _TypeAlias

ColorValue: _TypeAlias = tuple[int, int, int]
_HexCode: _TypeAlias = str


def rgb_color(red: int = 0, green: int = 0, blue: int = 0) -> ColorValue:
    """Creates a color from the given channels, which is red, green and blue

    Args:
        red (int, optional): red color channel. Defaults to 0.
        green (int, optional): green color channel. Defaults to 0.
        blue (int, optional): blue color channel. Defaults to 0.

    Returns:
        ColorValue: rgb color as tuple of 3 ints
    """
    return (red, green, blue)


def hex_color(hex_code: _HexCode = "#ffffff", /) -> ColorValue:
    """Creates a color from the given hex code. The "#" in the hex codes are optional

    Args:
        fg (_HexCode, optional): foreground hex color. Defaults to "#ffffff".

    Returns:
        ColorValue: rgb color as tuple of 3 ints
    """
    hex_code = hex_code.lower()
    if hex_code.startswith("#"):
        hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = ''.join([channel * 2 for channel in hex_code])
    
    red = int(hex_code[0:2], 16)
    green = int(hex_code[2:4], 16)
    blue = int(hex_code[4:6], 16)
    return (red, green, blue)


def rand_color() -> ColorValue:
    """Creates a random RGB color. Random background color is optional

    Returns:
        ColorValue: rgb color as tuple of 3 ints
    """
    return (
        _random.randint(0, 255),
        _random.randint(0, 255),
        _random.randint(0, 255)
    )


# standard colors:
BLACK   = (0,   0,   0  )
RED     = (255, 0,   0  )
GREEN   = (0,   255, 0  )
YELLOW  = (255, 255, 0  )
BLUE    = (0,   0,   255)
MAGENTA = (255, 0,   255)
CYAN    = (0,   255, 255)
WHITE   = (255, 255, 255)

# html/css colors:
ALICE_BLUE = (240, 248, 255)
ANTIQUE_WHITE = (250, 235, 215)
AQUA = (0, 255, 255)
AQUAMARINE = (127, 255, 212)
AZURE = (240, 255, 255)
BEIGE = (245, 245, 220)
BISQUE = (255, 228, 196)
BLANCHED_ALMOND = (255, 235, 205)
BLUE_VIOLET = (138, 43, 226)
BROWN = (165, 42, 42)
BURLY_WOOD = (222, 184, 135)
CADET_BLUE = (95, 158, 160)
CHARTREUSE = (127, 255, 0)
CHOCOLATE = (210, 105, 30)
CORAL = (255, 127, 80)
CORNFLOWER_BLUE = (100, 149, 237)
CORNSILK = (255, 248, 220)
CRIMSON = (220, 20, 60)
DARK_BLUE = (0, 0, 139)
DARK_CYAN = (0, 139, 139)
DARK_GOLDENROD = (184, 134, 11)
DARK_GRAY = (169, 169, 169)
DARK_GREEN = (0, 100, 0)
DARK_KHAKI = (189, 183, 107)
DARK_MAGENTA = (139, 0, 139)
DARK_OLIVE_GREEN = (85, 107, 47)
DARK_ORANGE = (255, 140, 0)
DARK_ORCHID = (153, 50, 204)
DARK_RED = (139, 0, 0)
DARK_SALMON = (233, 150, 122)
DARK_SEA_GREEN = (143, 188, 143)
DARK_SLATE_BLUE = (72, 61, 139)
DARK_SLATE_GRAY = (47, 79, 79)
DARK_TURQUOISE = (0, 206, 209)
DARK_VIOLET = (148, 0, 211)
DEEP_PINK = (255, 20, 147)
DEEP_SKY_BLUE = (0, 191, 255)
DIM_GRAY = (105, 105, 105)
DODGER_BLUE = (30, 144, 255)
FIREBRICK = (178, 34, 34)
FLORAL_WHITE = (255, 250, 240)
FOREST_GREEN = (34, 139, 34)
FUCHSIA = (255, 0, 255)
GAINSBORO = (220, 220, 220)
GHOST_WHITE = (248, 248, 255)
GOLD = (255, 215, 0)
GOLDENROD = (218, 165, 32)
GRAY = (128, 128, 128)
GREEN_YELLOW = (173, 255, 47)
HONEYDEW = (240, 255, 240)
HOT_PINK = (255, 105, 180)
INDIAN_RED = (205, 92, 92)
INDIGO = (75, 0, 130)
IVORY = (255, 255, 240)
KHAKI = (240, 230, 140)
LAVENDER = (230, 230, 250)
LAVENDER_BLUSH = (255, 240, 245)
LAWN_GREEN = (124, 252, 0)
LEMON_CHIFFON = (255, 250, 205)
LIGHT_BLUE = (173, 216, 230)
LIGHT_CORAL = (240, 128, 128)
LIGHT_CYAN = (224, 255, 255)
LIGHT_GOLDENROD_YELLOW = (250, 250, 210)
LIGHT_GRAY = (211, 211, 211)
LIGHT_GREEN = (144, 238, 144)
LIGHT_PINK = (255, 182, 193)
LIGHT_SALMON = (255, 160, 122)
LIGHT_SEA_GREEN = (32, 178, 170)
LIGHT_SKY_BLUE = (135, 206, 250)
LIGHT_SLATE_GRAY = (119, 136, 153)
LIGHT_STEEL_BLUE = (176, 196, 222)
LIGHT_YELLOW = (255, 255, 224)
LIME = (0, 255, 0)
LIME_GREEN = (50, 205, 50)
LINEN = (250, 240, 230)
MAROON = (128, 0, 0)
MEDIUM_AQUAMARINE = (102, 205, 170)
MEDIUM_BLUE = (0, 0, 205)
MEDIUM_ORCHID = (186, 85, 211)
MEDIUM_PURPLE = (147, 112, 219)
MEDIUM_SEA_GREEN = (60, 179, 113)
MEDIUM_SLATE_BLUE = (123, 104, 238)
MEDIUM_SPRING_GREEN = (0, 250, 154)
MEDIUM_TURQUOISE = (72, 209, 204)
MEDIUM_VIOLET_RED = (199, 21, 133)
MIDNIGHT_BLUE = (25, 25, 112)
MINT_CREAM = (245, 255, 250)
MISTY_ROSE = (255, 228, 225)
MOCCASIN = (255, 228, 181)
NAVAJO_WHITE = (255, 222, 173)
NAVY = (0, 0, 128)
OLD_LACE = (253, 245, 230)
OLIVE = (128, 128, 0)
OLIVE_DRAB = (107, 142, 35)
ORANGE = (255, 165, 0)
ORANGE_RED = (255, 69, 0)
ORCHID = (218, 112, 214)
PALE_GOLDENROD = (238, 232, 170)
PALE_GREEN = (152, 251, 152)
PALE_TURQUOISE = (175, 238, 238)
PALE_VIOLET_RED = (219, 112, 147)
PAPAYA_WHIP = (255, 239, 213)
PEACH_PUFF = (255, 218, 185)
PERU = (205, 133, 63)
PINK = (255, 192, 203)
PLUM = (221, 160, 221)
POWDER_BLUE = (176, 224, 230)
PURPLE = (128, 0, 128)
ROSY_BROWN = (188, 143, 143)
ROYAL_BLUE = (65, 105, 225)
SADDLE_BROWN = (139, 69, 19)
SALMON = (250, 128, 114)
SANDY_BROWN = (244, 164, 96)
SEA_GREEN = (46, 139, 87)
SEA_SHELL = (255, 245, 238)
SIENNA = (160, 82, 45)
SILVER = (192, 192, 192)
SKY_BLUE = (135, 206, 235)
SLATE_BLUE = (106, 90, 205)
SLATE_GRAY = (112, 128, 144)
SNOW = (255, 250, 250)
SPRING_GREEN = (0, 255, 127)
STEEL_BLUE = (70, 130, 180)
TAN = (210, 180, 140)
TEAL = (0, 128, 128)
THISTLE = (216, 191, 216)
TOMATO = (255, 99, 71)
TURQUOISE = (64, 224, 208)
VIOLET = (238, 130, 238)
WHEAT = (245, 222, 179)
WHITE_SMOKE = (245, 245, 245)
YELLOW_GREEN = (154, 205, 50)
