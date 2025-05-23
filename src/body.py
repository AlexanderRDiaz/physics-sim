from __future__ import annotations

from abc import abstractmethod

import math

from matrix import Vector, Transform


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
        mass: float,
        restitution: float,
        static: bool,
    ):
        self.Position = position
        self.LinearVelocity = Vector.Zero()
        self.Rotation = 0.0
        self.RotationalVelocity = 0.0

        self.Density = density
        self.Mass = mass
        self.Restitution = restitution

        self.Static = static

    @abstractmethod
    def Move(self: Body, distance: Vector):
        pass

    @abstractmethod
    def MoveTo(self: Body, position: Vector):
        pass

    @abstractmethod
    def Rotate(self: Body, amount: int | float):
        pass


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
        mass: float,
        restitution: float,
        static: bool,
    ):
        Body.__init__(
            self,
            position,
            density,
            mass,
            restitution,
            static,
        )
        self.Radius = radius
        self.Area = math.pi * radius * radius

    def Move(self: CircleBody, distance: Vector):
        self.Position += distance

    def MoveTo(self: CircleBody, position: Vector):
        self.Position = position

    def Rotate(self: CircleBody, amount: int | float):
        self.Rotation += amount


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

    Vertices: list[Vector]
    TriangulatedVertices: list[int]
    TransformedVertices: list[Vector]
    TransformUpdateRequired: bool

    def __init__(  # noqa: PLR0913
        self: BoxBody,
        width: float,
        height: float,
        position: Vector,
        density: float,
        mass: float,
        restitution: float,
        static: bool,
    ):
        Body.__init__(
            self,
            position,
            density,
            mass,
            restitution,
            static,
        )
        self.Width = width
        self.Height = height

        self.Vertices = self.__CreateVertices()
        self.TriangulatedVertices = [0, 1, 2, 0, 2, 3]
        self.TransformUpdateRequired = True

    def Move(self: BoxBody, distance: Vector):
        self.Position += distance
        self.TransformUpdateRequired = True

    def MoveTo(self: BoxBody, position: Vector):
        self.Position = position
        self.TransformUpdateRequired = True

    def Rotate(self: BoxBody, amount: int | float):
        self.Rotation += amount

    def GetTransformedVertices(self: BoxBody):
        if self.TransformUpdateRequired:
            self.TransformedVertices = __TransformVertices(
                self.Vertices,
                self.Position,
                self.Rotation,
            )
            self.TransformUpdateRequired = False

    def __CreateVertices(self: BoxBody) -> list[Vector]:
        left = -self.Width / 2
        right = left + self.Width
        bottom = -self.Height / 2
        top = bottom + self.Height

        return [
            Vector(left, top),
            Vector(left, bottom),
            Vector(right, top),
            Vector(right, bottom),
        ]


def __TransformVertices(vertices: list[Vector], position: Vector, rotation: float) -> list[Vector]:
    t = Transform.FromVector(position, rotation)

    return [Vector.Transform(v, t) for v in vertices]
