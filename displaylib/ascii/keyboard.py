from __future__ import annotations as _annotations

from typing import TypeAlias as _TypeAlias

_Key: _TypeAlias = int | str


def is_pressed(key: _Key, /) -> bool:
    # TODO: make implementation
    return False


try:
    import keyboard as _keyboard
    from keyboard import * # type: ignore

    # overriden interface for keyboard.is_pressed
    def is_pressed(key: _Key, /) -> bool:
        return _keyboard.is_pressed(key)


except ModuleNotFoundError:
    import os as _os
    
    if _os.name == "nt":  # Windows
        import msvcrt as _msvcrt

        _key_to_scancode: dict[str, int] = {
            # defined at runtime to match keys on physical keyboard better
            "0": ord("0"),
            "1": ord("1"),
            "2": ord("2"),
            "3": ord("3"),
            "4": ord("4"),
            "5": ord("5"),
            "6": ord("6"),
            "7": ord("7"),
            "8": ord("8"),
            "9": ord("9"),
            "space": ord(" "),
            "enter": ord("\r"),
            "del": ord("\b"),
            "delete": ord("\b"),
            "tab": ord("\t"),
            "bar": ord("|"),
            "esc": ord("\x1b"),
            "escape": ord("\x1b")
        }

        def is_pressed(key: _Key, /) -> bool:
            if isinstance(key, str):
                key = key.lower()
                if key in _key_to_scancode:
                    scancode = _key_to_scancode[key]
                elif len(key) == 1:
                    scancode = ord(key)
                else:
                    raise ValueError(f"key '{key}' of type 'str' was not recognized")
            elif isinstance(key, int):
                scancode = key
            else:
                raise ValueError("parameter 'key' has to be of type 'int' or 'str'")
            all_pressed = []
            while _msvcrt.kbhit():
                pressed = _msvcrt.getch()
                all_pressed.append(pressed)
                if ord(pressed) == scancode or (ord(pressed) + 32 == scancode and 65 <= ord(pressed) <= 90):
                    all_pressed.pop()
                    for prev_pressed in reversed(all_pressed):
                        try:
                            _msvcrt.ungetch(prev_pressed)
                        except OSError:
                            continue
                    return True
            for prev_pressed in reversed(all_pressed):
                try:
                    _msvcrt.ungetch(prev_pressed)
                except OSError:
                    continue
            return False
    
    
    # elif _os.name == "posix":  # Linux and macOS
    #     pass
    
    # else: use default functions that returns False as defaults
