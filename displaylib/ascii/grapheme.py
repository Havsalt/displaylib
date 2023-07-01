"""### Grapheme cluster utility module

Provides functions related to alter text
"""

from __future__ import annotations as _annotations

__all__ = [
    "Conversion",
    "lookuph",
    "lookupv",
    "fliph",
    "flipv",
    "mapfliph",
    "mapflipv",
    "rotate"
]

from collections.abc import Iterable as _Iterable
from math import pi as _PI


class Conversion: # holds the translate information
    horizontal: dict[str, str] = { # horizontal flip
        "/": "\\",
        "(": ")",
        "[": "]",
        "{": "}",
        ">": "<",
        "´": "`",
        "d": "b"
    }
    vertical: dict[str, str] = { # vertical flip
        "/": "\\",
        ".": "'",
        "¨": "_",
        "b": "p",
        "w": "m",
        "W": "M",
        "v": "^",
        "V": "A"
    }
    rotational: dict[str, list[str]] = { # rotational adjusted
        "|": ["|", "\\", "-", "/", "|", "\\", "-", "/"],
        ".": [".", "'"]
    }

# -- mirror database
for key, value in tuple(Conversion.horizontal.items()):
    Conversion.horizontal[value] = key
for key, value in tuple(Conversion.vertical.items()):
    Conversion.vertical[value] = key
# for key, options in tuple(Conversion.rotational.items()):
#     for idx, option in enumerate(options):
#         new_key = options[idx]
#         new_options = options[idx:] + options[:idx]
#         Conversion.rotational[new_key] = new_options

# --- module functions
def lookuph(symbol: str) -> str:
    """Lookup a symbol from the `horizontal` database

    Args:
        symbol (str): symbol to lookup

    Returns:
        str: result or symbol supplied
    """
    return Conversion.horizontal.get(symbol, symbol)


def lookupv(symbol: str) -> str:
    """Lookup a symbol from the `vertical` database

    Args:
        symbol (str): symbol to lookup

    Returns:
        str: result or symbol supplied
    """
    return Conversion.vertical.get(symbol, symbol)


def fliph(line: str | _Iterable[str]) -> str:
    """Flip a line of text `horizontally`

    Args:
        line (str | Iterable[str]): text line or iterable of strings with string length of 1

    Returns:
        str: line flipped horizontally
    """
    return "".join(Conversion.horizontal.get(letter, letter) for letter in line)[::-1]


def flipv(line: str | _Iterable[str]) -> str:
    """Flip a line of text `vertically`

    Args:
        line (str | Iterable[str]): text line or iterable of strings with string length of 1

    Returns:
        str: line flipped vertically
    """
    return "".join(Conversion.vertical.get(letter, letter) for letter in line)


def mapfliph(content: _Iterable[str | _Iterable[str]]) -> list[str]:
    """Flip a list with text lines `horizontally`

    Args:
        line (content: Iterable[str | Iterable[str]]): list with: text lines | list with iterables of strings with string length of 1

    Returns:
        str: list with lines flipped horizontally
    """
    return [fliph(line) for line in content]


def mapflipv(content: _Iterable[str | _Iterable[str]]) -> list[str]:
    """Flip a list with text lines `vertically`

    Args:
        line (content: Iterable[str | Iterable[str]]): list with: text lines | list with iterables of strings with string length of 1

    Returns:
        str: list with lines flipped vertically
    """
    return [flipv(line) for line in content][::-1]


def rotate(symbol: str, angle: float) -> str:
    """Returns a symbol when rotating it with the given angle

    Args:
        symbol (str): symbol to rotate
        angle (float): counter clockwise rotation

    Returns:
        str: rotated symbol or original symbol
    """
    if symbol in Conversion.rotational:
        options = len(Conversion.rotational[symbol])
        index = round(((angle % _PI) / (2*_PI)) * options)
        return Conversion.rotational[symbol][index]
    
    for idx, options in enumerate(Conversion.rotational.values()):
        if symbol in options:
            break
    else: # nobreak
        return symbol
    key = list(Conversion.rotational.keys())[idx]
    options = Conversion.rotational[key]
    where = options.index(symbol)
    length = len(options)
    index = round(((angle % _PI) / (2*_PI)) * length) -where
    return Conversion.rotational[key][index]
