from __future__ import annotations

from math import sqrt, floor, ceil, cos, sin, atan2, inf as INF
from typing import Iterator, Literal, Any

from typing_extensions import Self

from ._numerical_tools import lerp, sign, clamp, move_toward
from ._class_constant import class_constant
from ._annotations import Radians


class Vec2:
    """`Vector2` data structure

    Components: `x`, `y`

    Usefull for storing position or direction
    """

    __slots__ = ("x", "y")

    @class_constant
    def ZERO(cls: type[Self]) -> Self:  # type: ignore
        """Vector with all components set to `0`"""
        return cls(0, 0)

    @class_constant
    def ONE(cls: type[Self]) -> Self:  # type: ignore
        """Vector with all components set to `1`"""
        return cls(1, 1)

    @class_constant
    def INF(cls: type[Self]) -> Self:  # type: ignore
        """Vector with all components set to `math.inf`"""
        return cls(INF, INF)

    @class_constant
    def LEFT(cls: type[Self]) -> Self:  # type: ignore
        """Left unit vector

        Represents the `left direction`
        """
        return cls(-1, 0)

    @class_constant
    def RIGHT(cls: type[Self]) -> Self:  # type: ignore
        """Right unit vector

        Represents the `right direction`
        """
        return cls(1, 0)

    @class_constant
    def UP(cls: type[Self]) -> Self:  # type: ignore
        """Up unit vector

        Represents the `up direction`

        NOTE: Y is down in 2D, so this vector points -Y
        """
        return cls(0, -1)

    @class_constant
    def DOWN(cls: type[Self]) -> Self:  # type: ignore
        """Down unit vector

        Represents the `down direction`

        NOTE: Y is down in 2D, so this vector points +Y
        """
        return cls(0, 1)

    @classmethod
    def from_angle(cls, angle: Radians, /) -> Self:
        """Create a direction vector of length 1 from given angle

        Args:
            angle (Radians): Angle in radians

        Returns:
            Self: Direction vector of length 1
        """
        x = cos(angle)
        y = sin(angle)
        return cls(x, y)

    def __init__(self, x: float, y: float, /) -> None:
        """Initialize vector

        Args:
            x (float): X component
            y (float): Y component
        """
        self.x = x
        self.y = y

    def __reduce__(self) -> tuple[type[Self], tuple[float, float]]:
        return (self.__class__, (self.x, self.y))

    def __len__(self) -> Literal[2]:
        return 2

    def __iter__(self) -> Iterator[float]:
        return iter((self.x, self.y))

    def __getitem__(self, item: Literal[0, 1]) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        raise ValueError(f"item '{item}' does not correspond to x or y axis")

    def __repr__(self) -> str:
        """Create representation

        Returns:
            str: Representation containing the x and y component
        """
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __str__(self) -> str:
        """Create string representation

        Returns:
            str: Representation containing the x and y component
        """
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __bool__(self) -> bool:
        """Return whether x or y is not zero

        Returns:
            bool: Truthiness
        """
        return bool(self.x or self.y)

    def __abs__(self) -> Self:
        return self.__class__(
            abs(self.x),
            abs(self.y),
        )

    def __round__(self, ndigits: int = 0) -> Self:
        return self.__class__(
            round(self.x, ndigits),
            round(self.y, ndigits),
        )

    def __floor__(self) -> Self:
        return self.__class__(
            floor(self.x),
            floor(self.y),
        )

    def __ceil__(self) -> Self:
        return self.__class__(
            ceil(self.x),
            ceil(self.y),
        )

    def __neg__(self) -> Vec2:
        return Vec2(-self.x, -self.y)

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vec2) -> Vec2:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vec2) -> Vec2:
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(
                self.x * other.x,
                self.y * other.y,
            )
        return Vec2(
            self.x * other,
            self.y * other,
        )

    def __imul__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self

    def __floordiv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(
                self.x // other.x,
                self.y // other.y,
            )
        return Vec2(
            self.x // other,
            self.y // other,
        )

    def __ifloordiv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            self.x //= other.x
            self.y //= other.y
        else:
            self.x //= other
            self.y //= other
        return self

    def __truediv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(
                self.x / other.x,
                self.y / other.y,
            )
        return Vec2(
            self.x / other,
            self.y / other,
        )

    def __itruediv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        return self

    def __mod__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(
                self.x % other.x,
                self.y % other.y,
            )
        return Vec2(
            self.x % other,
            self.y % other,
        )

    def __imod__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            self.x %= other.x
            self.y %= other.y
        else:
            self.x %= other
            self.y %= other
        return self

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

    def __copy__(self) -> Self:
        return self.__class__(self.x, self.y)

    def __deepcopy__(self, _memo: dict[int, Any]) -> Self:
        return self.__class__(self.x, self.y)

    def copy(self) -> Self:
        """Return a vector copy

        Returns:
            Self: A new copy
        """
        return self.__copy__()

    def length(self) -> float:
        """Return the length of the vector

        Returns:
            float: Length
        """
        if self.x == 0 and self.y == 0:
            return 0
        return sqrt(self.x * self.x + self.y * self.y)

    def length_squared(self) -> float:
        """Return the length of the vector squared

        Returns:
            float: Length squared
        """
        if self.x == 0 and self.y == 0:
            return 0
        return self.x * self.x + self.y * self.y

    def distance_to(self, other: Vec2, /) -> float:
        """Return the relative distance to the other point

        Args:
            other (Vec2): Other point

        Returns:
            float: Distance
        """
        return (other - self).length()

    def distance_squared_to(self, other: Vec2, /) -> float:
        """Return the relative distance to the other point, squared

        Args:
            other (Vec2): Other point

        Returns:
            float: Distance squared
        """
        return (other - self).length_squared()

    def normalized(self) -> Vec2:
        """Return a vector with length of 1, still with same direction

        Returns:
            Vec2: Normalized vector
        """
        length = self.length()
        if length == 0:
            return Vec2(0, 0)
        return self / self.length()

    def dot(self, other: Vec2, /) -> float:
        """Return the dot product between two 2D vectors

        Args:
            other (Vec2): Other vector

        Returns:
            float: Dot product
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vec2, /) -> float:
        """Cross product interpreted in 2D space, like defined in the `Godot Game Engine`

        Args:
            other (Vec2): other vector

        Returns:
            float: cross product
        """
        return self.x * other.y - self.y * other.x

    def direction_to(self, other: Vec2, /) -> Vec2:
        """Return the direction to the other point

        Args:
            other (Vec2): other point

        Returns:
            Vec2: direction
        """
        return (other - self).normalized()

    def angle(self, /) -> float:
        """Return the angle (measured in radians), using `atan2`

        Returns:
            float: Angle given in radians
        """
        return atan2(self.y, self.x)

    def angle_to(self, other: Vec2, /) -> float:
        """Return the angle (measured in radians) to the other point

        Args:
            other (Vec2): Other point

        Returns:
            float: Angle given in radians
        """
        return (other - self).angle()

    def lerp(self, target: Vec2, /, weight: float) -> Vec2:
        """Lerp towards vector `target` with `weight` ranging from 0 to 1

        Args:
            target (Vec2): Target to lerp towards
            weight (float): Percentage to lerp

        Returns:
            Vec2: Vector after performing interpolation
        """
        return Vec2(
            lerp(self.x, target.x, weight),
            lerp(self.y, target.y, weight),
        )

    def sign(self) -> Vec2:
        """Return a Vec2 with each component being the sign of the vector

        Returns:
            Vec2: Vector with signed components
        """
        return Vec2(
            sign(self.x),
            sign(self.y),
        )

    def clamp(self, smallest: Vec2, largest: Vec2, /) -> Vec2:
        """Return a new clamped vector

        Args:
            smallest (Vec2): Lower bound for x and y
            largest (Vec2): Upper bound for x and y

        Returns:
            Vec2: Vector clamped
        """
        return Vec2(
            clamp(self.x, smallest.x, largest.x),
            clamp(self.y, smallest.y, largest.y),
        )

    def move_toward(self, stop: Vec2, /, change: int | float) -> Vec2:
        """Move toward a vector, from a vector, with given change

        Args:
            stop (Vec2): Target vector
            change (int | float): Max distance to move

        Returns:
            Vec2: New vector moved
        """
        return Vec2(
            move_toward(self.x, stop.x, change),
            move_toward(self.y, stop.y, change),
        )

    def rotated(self, angle: float, /) -> Vec2:
        """Return a vector rotated clockwise by `angle` given in radians

        Args:
            angle (float): Radians to rotate with

        Returns:
            Vec2: Rotated vector
        """
        cos_rad = cos(angle)
        sin_rad = sin(angle)
        x = cos_rad * self.x + sin_rad * self.y
        y = -sin_rad * self.x + cos_rad * self.y
        return Vec2(x, y)

    def rotated_around(self, angle: float, point: Vec2) -> Vec2:
        """Return a vector rotated by `angle` given in radians, around `point`

        Args:
            angle (float): Radians to rotate with
            point (Vec2): Point to rotate around

        Returns:
            Vec2: Vector rotated around `point`
        """
        diff = self - point
        cos_rad = cos(angle)
        sin_rad = sin(angle)
        x = point.x + cos_rad * diff.x + sin_rad * diff.y
        y = point.y + -sin_rad * diff.x + cos_rad * diff.y
        return Vec2(x, y)
