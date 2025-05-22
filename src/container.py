from __future__ import annotations

import math

from body import Body
from matrix import Vector

import JES
import enums as Enums
import mathlib
import settings


class Container:
    Bodies: list[Body]

    def __init__(self: Container):
        self.Bodies = []
        self.CreateCircleBody(
            Vector(20, 20),
            40.0,
            1.0,
            True,
            0.2,
        )

    def StepTime(self: Container):
        canvas = JES.makeEmptyPicture(400, 400)
        for body in self.Bodies:
            if body.ShapeType == Enums.ShapeType.Circle:
                x, y = body.Position.X - (body.Radius / 2), body.Position.Y - (body.Radius / 2)
                JES.addOvalFilled(canvas, x, y, body.Radius, body.Radius)
        JES.writePictureTo(canvas, 'test.jpg')

    def CreateCircleBody(  # noqa: PLR0913
        self: Container,
        position: Vector,
        radius: float,
        density: float,
        static: bool,
        restitution: float,
    ) -> None:
        area = radius * radius * math.pi

        if not (settings.MIN_BODY_SIZE <= area <= settings.MAX_BODY_SIZE):
            raise RuntimeError(
                f'Circle area lies outside of the designated range, area is {area} cm^2',
            )

        if not (settings.MIN_DENSITY <= density <= settings.MAX_DENSITY):
            raise RuntimeError(
                f'Density lies outside of the designated range, density is {density} g/cm^3',
            )

        restitution = mathlib.Clamp(restitution, 0.0, 1.0)
        mass = area * density

        self.Bodies.append(
            Body(
                position,
                density,
                mass,
                restitution,
                area,
                static,
                radius,
                0.0,
                0.0,
                Enums.ShapeType.Circle,
            ),
        )

    def CreateBoxBody(  # noqa: PLR0913
        self: Container,
        position: Vector,
        width: float,
        height: float,
        density: float,
        static: bool,
        restitution: float,
    ) -> None:
        area = width * height

        if not (settings.MIN_BODY_SIZE <= area <= settings.MAX_BODY_SIZE):
            raise RuntimeError(
                f'Box area lies outside of the designated range, area is {area} cm^2',
            )

        if not (settings.MIN_DENSITY <= density <= settings.MAX_DENSITY):
            raise RuntimeError(
                f'Density lies outside of the designated range, density is {density} g/cm^3',
            )

        restitution = mathlib.Clamp(restitution, 0.0, 1.0)
        mass = area * density

        self.Bodies.append(
            Body(
                position,
                density,
                mass,
                restitution,
                area,
                static,
                0.0,
                width,
                height,
                Enums.ShapeType.Box,
            ),
        )
