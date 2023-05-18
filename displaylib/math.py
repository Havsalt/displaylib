from __future__ import annotations

from math import sqrt, cos, sin, atan2

__all__ = [
    "lerp",
    "sign",
    "Vec2",
    "Vec2i"
]


def lerp(start: int | float, end: int | float, weight: float, /) -> float:
    """Lerps between `start` and `end` with `weight` ranging from 0 to 1

    Args:
        start (int | float): starting number
        end (int | float): target number
        weight (float): percentage to lerp

    Returns:
        float: result of the interpolation
    """
    return (1 - weight) * start + (weight * end)


def sign(number: int | float, /) -> int:
    """Returns the sign of the number. The number 0 will return 0

    Args:
        number (int | float): number to get the sign of

    Returns:
        int: sign
    """
    return 0 if number == 0 else (1 if number > 0 else -1)


class Vec2: # TODO: add support for network notify protocol
    """`Vector2` data structure

    Components: `x`, `y`

    Usefull for storing position or direction
    """
    __slots__ = ("x", "y")

    def __init__(self, x: int | float = 0, y: int | float = 0, /) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Representation with class name an memory address

        Returns:
            str: representation of the vector
        """
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"
    
    def __str__(self) -> str:
        """String representation

        Returns:
            str: representation containing the x and y component
        """
        return f"Vec2({self.x}, {self.y})"
    
    def __round__(self, ndigits: int = 0) -> Vec2:
        return Vec2(round(self.x, ndigits),
                    round(self.y, ndigits))
    
    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x,
                    self.y + other.y)
    
    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x,
                    self.y - other.y)

    def __mul__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x,
                        self.y * other.y)
        return Vec2(self.x * other,
                    self.y * other)
    
    def __floordiv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x // other.x,
                        self.y // other.y)
        return Vec2(self.x // other,
                    self.y // other)
    
    def __truediv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x,
                        self.y / other.y)
        return Vec2(self.x / other,
                    self.y / other)
    
    def __mod__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x % other.x,
                        self.y % other.y)
        return Vec2(self.x % other,
                    self.y % other)
    
    def __eq__(self, other: Vec2) -> bool:
        return (self.x == other.x) and (self.y == other.y)
    
    def __ne__(self, other: Vec2) -> bool:
        return (self.x != other.x) or (self.y != other.y)
    
    def __gt__(self, other: Vec2) -> bool:
        return (self.x > other.x) and (self.y > other.y)
    
    def __lt__(self, other: Vec2) -> bool:
        return (self.x < other.x) and (self.y < other.y)
    
    def __ge__(self, other: Vec2) -> bool:
        return (self.x >= other.x) and (self.y >= other.y)

    def __le__(self, other: Vec2) -> bool:
        return (self.x <= other.x) and (self.y <= other.y)

    def __serialize__(self) -> str:
        return f"{self.__class__.__qualname__}({self.x}, {self.y})"

    def length(self) -> float:
        """Returns the length of the vector

        Returns:
            float: length
        """
        if self.x == 0 and self.y == 0:
            return 0.0
        return sqrt(self.x*self.x + self.y*self.y)
    
    def normalized(self) -> Vec2:
        """Returns a vector with length of 1, still with same direction

        Returns:
            Vec2: normalized vector
        """
        length = self.length()
        if length == 0:
            return Vec2(0, 0)
        return self / self.length()

    def angle(self) -> float:
        """Returns the angle (measured in radians), using atan2

        Returns:
            float: angle given in radians
        """
        return atan2(self.y, self.x)

    def lerp(self, target: Vec2, weight: int | float, /) -> Vec2:
        """Lerp towards vector `target` with `weight` ranging from 0 to 1

        Args:
            target (Vec2): _description_
            weight (int | float): percentage to lerp

        Returns:
            Vec2: vector after performing interpolation
        """
        return Vec2(lerp(self.x, target.x, weight),
                    lerp(self.y, target.y, weight))

    def sign(self) -> Vec2:
        """Returns a Vec2 with each component being the sign of the vector

        Returns:
            Vec2: vector with signed components
        """
        return Vec2(sign(self.x), sign(self.y))
    
    def rotated(self, angle: float, /) -> Vec2:
        """Returns a vector rotated by `angle` given in radians

        Args:
            angle (float): radians to rotate with

        Returns:
            Vec2: rotated vector
        """
        cos_rad = cos(angle)
        sin_rad = sin(angle)
        x = cos_rad * self.x + sin_rad * self.y
        y = -sin_rad * self.x + cos_rad * self.y
        return Vec2(x, y)
    
    def rotated_around(self, angle: float, point: Vec2, /) -> Vec2:
        """Returns a vector rotated by `angle` given in radians, around `point`

        Args:
            angle (float): radians to rotate with
            point (Vec2): point to rotate around

        Returns:
            Vec2: vector rotated around `point`
        """
        diff = self - point
        cos_rad = cos(angle)
        sin_rad = sin(angle)
        x = point.x + cos_rad * diff.x + sin_rad * diff.y
        y = point.y + -sin_rad * diff.x + cos_rad * diff.y
        return Vec2(x, y)


class Vec2i(Vec2):
    """`Vector2 integer` data structure

    Components: `x`, `y` only type `int`

    Usefull for storing whole numbers in 2D space
    """
    __slots__ = ("x", "y")

    def __init__(self, x: int = 0, y: int = 0, /) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, other: Vec2i | Vec2) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x + other.x),
                         int(self.y + other.y))
        return Vec2(self.x + other.x,
                    self.y + other.y)
    
    def __sub__(self, other: Vec2i | Vec2) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x - other.x),
                         int(self.y - other.y))
        return Vec2(self.x - other.x,
                    self.y - other.y)

    def __mul__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x * other.x),
                         int(self.y * other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x * other.x,
                        self.y * other.y)
        return Vec2(self.x * other,
                    self.y * other)
    
    def __floordiv__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(self.x // other.x,
                         self.y // other.y)
        elif isinstance(other, Vec2):
            return Vec2(self.x // other.x,
                        self.y // other.y)
        return Vec2(self.x * other,
                    self.y * other)
    
    def __truediv__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x / other.x),
                         int(self.y / other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x / other.x,
                        self.y / other.y)
        return Vec2(self.x / other,
                    self.y / other)
    
    def __mod__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x % other.x),
                         int(self.y % other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x % other.x,
                        self.y % other.y)
        return Vec2(self.x % other,
                    self.y % other)
