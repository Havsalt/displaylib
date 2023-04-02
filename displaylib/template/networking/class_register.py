from __future__ import annotations

from ...math import Vec2, Vec2i # pre-registered


cache: dict[str, type] = {
    "Vec2": Vec2,
    "Vec2i": Vec2i
}


def register_class(cls: type) -> None:
    """Register a class so it can be used in `deserialize` to create an instance of the given class

    Args:
        type (type): class to register
    """
    cache[cls.__name__] = cls
