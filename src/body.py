from __future__ import annotations

from matrix import Vector

import enums as Enums


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
        'Radius',
        'Width',
        'Height',
        'ShapeType',
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

    Radius: float
    Width: float
    Height: float

    ShapeType: Enums.ShapeType
    Vertices: list[Vector] | None

    def __init__(  # noqa: PLR0913
        self: Body,
        position: Vector,
        density: float,
        mass: float,
        restitution: float,
        area: float,
        static: bool,
        radius: float,
        width: float,
        height: float,
        shapeType: Enums.ShapeType,
    ):
        self.Position = position
        self.LinearVelocity = Vector.Zero()
        self.Rotation = 0.0
        self.RotationalVelocity = 0.0

        self.Density = density
        self.Mass = mass
        self.Restitution = restitution
        self.Area = area

        self.Static = static

        self.Radius = radius
        self.Width = width
        self.Height = height

        self.ShapeType = shapeType

    def Move(self: Body, amount: Vector):
        self.Position += amount

    def MoveTo(self: Body, position: Vector):
        self.Position = position

    def __CreateBoxVertices(self: Body, width: float, height: float) -> None:
        left = -width / 2
        right = left + width
        bottom = -height / 2
        top = bottom + height

        vertices = [
            Vector(left, top),
            Vector(left, bottom),
            Vector(right, top),
            Vector(right, bottom),
        ]
