"""### Grapheme cluster utility module

Provides functions related to alter text
"""

from __future__ import annotations

__all__ = [
    "Database",
    "lookuph",
    "lookupv",
    "fliph",
    "flipv",
    "mapfliph",
    "mapflipv",
    "rotate"
]

from collections.abc import Iterable
from math import pi as PI

# -- database
class Database:
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
for key, value in tuple(Database.horizontal.items()):
    Database.horizontal[value] = key
for key, value in tuple(Database.vertical.items()):
    Database.vertical[value] = key
# for key, options in tuple(Database.rotational.items()):
#     for idx, option in enumerate(options):
#         new_key = options[idx]
#         new_options = options[idx:] + options[:idx]
#         Database.rotational[new_key] = new_options

# --- module functions
def lookuph(symbol: str) -> str:
    """Lookup a symbol from the `horizontal` database

    Args:
        symbol (str): symbol to lookup

    Returns:
        str: result or symbol supplied
    """
    return Database.horizontal.get(symbol, symbol)


def lookupv(symbol: str) -> str:
    """Lookup a symbol from the `vertical` database

    Args:
        symbol (str): symbol to lookup

    Returns:
        str: result or symbol supplied
    """
    return Database.vertical.get(symbol, symbol)


def fliph(line: str | Iterable[str]) -> str:
    """Flip a line of text `horizontally`

    Args:
        line (str | Iterable[str]): text line or iterable of strings with string length of 1

    Returns:
        str: line flipped horizontally
    """
    return "".join(Database.horizontal.get(letter, letter) for letter in line)[::-1]


def flipv(line: str | Iterable[str]) -> str:
    """Flip a line of text `vertically`

    Args:
        line (str | Iterable[str]): text line or iterable of strings with string length of 1

    Returns:
        str: line flipped vertically
    """
    return "".join(Database.vertical.get(letter, letter) for letter in line)


def mapfliph(content: Iterable[str | Iterable[str]]) -> list[str]:
    """Flip a list with text lines `horizontally`

    Args:
        line (content: Iterable[str | Iterable[str]]): list with: text lines | list with iterables of strings with string length of 1

    Returns:
        str: list with lines flipped horizontally
    """
    return [fliph(line) for line in content]


def mapflipv(content: Iterable[str | Iterable[str]]) -> list[str]:
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
    if symbol in Database.rotational:
        options = len(Database.rotational[symbol])
        index = round(((angle % PI) / (2*PI)) * options)
        return Database.rotational[symbol][index]
    
    for idx, options in enumerate(Database.rotational.values()):
        if symbol in options:
            break
    else: # nobreak
        return symbol
    key = list(Database.rotational.keys())[idx]
    options = Database.rotational[key]
    where = options.index(symbol)
    length = len(options)
    index = round(((angle % PI) / (2*PI)) * length) -where
    return Database.rotational[key][index]
