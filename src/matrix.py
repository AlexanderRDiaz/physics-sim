from __future__ import annotations

from dataclasses import dataclass

import math


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
    def Zero():
        return Vector(0, 0)

    @staticmethod
    def Length(v: Vector):
        return math.sqrt((v.X * v.X) + (v.Y * v.Y))

    @staticmethod
    def Distance(a: Vector, b: Vector):
        dx = a.X - b.X
        dy = a.Y - b.Y
        return math.sqrt((dx * dx) + (dy * dy))

    @staticmethod
    def Normal(v: Vector):
        _len_ = Vector.Length(v)
        return Vector(v.X / _len_, v.Y / _len_)

    @staticmethod
    def Dot(a: Vector, b: Vector):
        return (a.X * b.X) + (a.Y * b.Y)

    @staticmethod
    def Cross(a: Vector, b: Vector):
        return (a.X * b.Y) - (a.Y * b.X)

    @staticmethod
    def Transform(v: Vector, t: Transform):
        return Vector(
            t.Cosine * v.X - t.Sine * v.Y + t.X,
            t.Sine * v.X + t.Cosine * v.Y + t.Y,
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

    def __init__(self: Transform, x: int | float, y: int | float, angle: int | float):
        self.X = x
        self.Y = y
        self.Sine = math.sin(angle)
        self.Cosine = math.cos(angle)

    @staticmethod
    def FromVector(position: Vector, angle: int | float):
        return Transform(position.X, position.Y, angle)

    @staticmethod
    def FromCoords(x: int | float, y: int | float, angle: int | float):
        return Transform(x, y, angle)

    @staticmethod
    def Zero():
        return Transform(0, 0, 0)
