from __future__ import annotations

import math

from abc import abstractmethod

from PIL import ImageDraw

from .matrix import Transform, Vector


class Body:
    __slots__ = [
        'Position',
        'LinearVelocity',
        'Rotation',
        'RotationalVelocity',
        'Density',
        'Mass',
        'Restitution',
        'Area',
        'Static',
    ]

    Position: Vector
    LinearVelocity: Vector
    Rotation: float
    RotationalVelocity: float

    Density: float
    Mass: float
    Restitution: float
    Area: float

    Static: bool

    @abstractmethod
    def __init__(  # noqa: PLR0913
        self: Body,
        position: Vector,
        density: float,
        restitution: float,
        static: bool,
    ) -> None:
        self.Position = position
        self.LinearVelocity = Vector.Zero()
        self.Rotation = 0.0
        self.RotationalVelocity = 0.0

        self.Density = density
        self.Restitution = restitution

        self.Static = static

    @abstractmethod
    def Draw(self: Body, draw: ImageDraw.ImageDraw) -> None:
        pass

    @abstractmethod
    def Move(self: Body, distance: Vector) -> None:
        pass

    @abstractmethod
    def MoveTo(self: Body, position: Vector) -> None:
        pass

    @abstractmethod
    def Rotate(self: Body, amount: int | float) -> None:
        pass


class BoxBody(Body):
    __slots__ = [
        'Width',
        'Height',
        'Vertices',
        'TriangulatedVertices',
        'TransformedVertices',
        'TransformUpdateRequired',
    ]

    Width: float
    Height: float

    Vertices: tuple[Vector, ...]
    TriangulatedVertices: tuple[int, ...]
    TransformedVertices: tuple[Vector, ...]
    TransformUpdateRequired: bool

    def __init__(  # noqa: PLR0913
        self: BoxBody,
        width: float,
        height: float,
        position: Vector,
        density: float,
        restitution: float,
        static: bool,
    ) -> None:
        Body.__init__(
            self,
            position,
            density,
            restitution,
            static,
        )
        self.Width = width
        self.Height = height
        self.Area = width * height
        self.Mass = self.Area * self.Density

        self.Vertices = self.__CreateVertices()
        self.TriangulatedVertices = (0, 1, 2, 0, 2, 3)
        self.TransformUpdateRequired = True

    def Draw(self: BoxBody, draw: ImageDraw.ImageDraw) -> None:
        draw.polygon(_VerticesToDrawFormat(self.GetTransformedVertices()), fill=0)

    def Move(self: BoxBody, distance: Vector) -> None:
        self.Position += distance
        self.TransformUpdateRequired = True

    def MoveTo(self: BoxBody, position: Vector) -> None:
        self.Position = position
        self.TransformUpdateRequired = True

    def Rotate(self: BoxBody, amount: int | float):
        self.Rotation += amount
        self.TransformUpdateRequired = True

    def GetTransformedVertices(self: BoxBody) -> tuple[Vector, ...]:
        if self.TransformUpdateRequired:
            self.TransformedVertices = _TransformVertices(
                self.Vertices,
                self.Position,
                self.Rotation,
            )
            self.TransformUpdateRequired = False

        return self.TransformedVertices

    def __CreateVertices(self: BoxBody) -> tuple[Vector, ...]:
        left = -self.Width / 2
        right = left + self.Width
        bottom = -self.Height / 2
        top = bottom + self.Height

        return (
            Vector(left, top),
            Vector(left, bottom),
            Vector(right, bottom),
            Vector(right, top),
        )


class CircleBody(Body):
    __slots__ = [
        'Radius',
    ]

    Radius: float

    def __init__(  # noqa: PLR0913
        self: CircleBody,
        radius: float,
        position: Vector,
        density: float,
        restitution: float,
        static: bool,
    ) -> None:
        Body.__init__(
            self,
            position,
            density,
            restitution,
            static,
        )
        self.Radius = radius
        self.Area = math.pi * radius * radius
        self.Mass = self.Area * self.Density

    def Move(self: CircleBody, distance: Vector) -> None:
        self.Position += distance

    def MoveTo(self: CircleBody, position: Vector) -> None:
        self.Position = position

    def Rotate(self: CircleBody, amount: int | float) -> None:
        self.Rotation += amount


def _TransformVertices(
    vertices: tuple[Vector, ...], position: Vector, rotation: float
) -> tuple[Vector, ...]:
    t = Transform.FromVector(position, rotation)

    return tuple([Vector.Transform(v, t) for v in vertices])


def _VerticesToDrawFormat(vertices: tuple[Vector, ...]):
    return tuple([(v.X, v.Y) for v in vertices])
