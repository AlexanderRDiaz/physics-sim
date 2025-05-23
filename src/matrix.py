from __future__ import annotations

import math

from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    X: int | float
    Y: int | float

    def __add__(self: Vector, obj) -> Vector:
        assert isinstance(obj, Vector), f'Cannot perform addition on Vector and {type(obj)}'
        return Vector(self.X + obj.X, self.Y + obj.Y)

    def __sub__(self: Vector, obj) -> Vector:
        assert isinstance(obj, Vector), f'Cannot perform subtraction on Vector and {type(obj)}'
        return Vector(self.X - obj.X, self.Y - obj.Y)

    def __mult__(self: Vector, s: int | float) -> Vector:
        return Vector(self.X * s, self.Y * s)

    def __div__(self: Vector, s: int | float) -> Vector:
        return Vector(self.X / s, self.Y / s)

    def __floordiv__(self: Vector, s: int | float) -> Vector:
        return Vector(self.X // s, self.Y // s)

    def __pos__(self: Vector) -> Vector:
        return Vector(
            -self.X if self.X < 0 else self.X,
            -self.Y if self.Y < 0 else self.Y,
        )

    def __neg__(self: Vector) -> Vector:
        return Vector(-self.X, -self.Y)

    def __eq__(self: Vector, other: object) -> bool:
        if not isinstance(other, Vector):
            return False

        return (self.X == other.X) and (self.Y == other.Y)

    @staticmethod
    def Zero() -> Vector:
        return Vector(0, 0)

    def Length(self: Vector) -> float:
        return math.sqrt((self.X * self.X) + (self.Y * self.Y))

    def Normal(self: Vector) -> Vector:
        _len_ = Vector.Length(self)
        return Vector(self.X / _len_, self.Y / _len_)

    def Distance(self: Vector, v: Vector) -> float:
        dx = self.X - v.X
        dy = self.Y - v.Y
        return math.sqrt((dx * dx) + (dy * dy))

    def Dot(self: Vector, v: Vector) -> int | float:
        return (self.X * v.X) + (self.Y * v.Y)

    def Cross(self: Vector, v: Vector) -> int | float:
        return (self.X * v.Y) - (self.Y * v.X)

    def Transform(self: Vector, t: Transform) -> Vector:
        return Vector(
            t.Cosine * self.X - t.Sine * self.Y + t.X,
            t.Sine * self.X + t.Cosine * self.Y + t.Y,
        )


class Transform:
    __slots__ = [
        'X',
        'Y',
        'Sine',
        'Cosine',
    ]

    X: int | float
    Y: int | float
    Sine: float
    Cosine: float

    def __init__(self: Transform, x: int | float, y: int | float, angle: int | float) -> None:
        self.X = x
        self.Y = y
        self.Sine = math.sin(angle)
        self.Cosine = math.cos(angle)

    @staticmethod
    def FromCoords(x: int | float, y: int | float, angle: int | float) -> Transform:
        return Transform(x, y, angle)

    @staticmethod
    def FromVector(position: Vector, angle: int | float) -> Transform:
        return Transform(position.X, position.Y, angle)

    @staticmethod
    def Zero() -> Transform:
        return Transform(0, 0, 0)
