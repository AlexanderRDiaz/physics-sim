from __future__ import annotations

from collections.abc import Callable

from PIL import Image, ImageDraw

from . import collisions
from .body import BoxBody, CircleBody
from .matrix import Vector


class World:
    __slots__ = [
        'Width',
        'Height',
        'Bodies',
        'Gravity',
        'Prerender',
        'OnCollide',
    ]

    Width: int
    Height: int

    Bodies: list[BoxBody | CircleBody]
    Gravity: Vector

    Prerender: Callable[..., None]
    OnCollide: Callable[..., None]

    def __init__(self: World) -> None:
        self.Width, self.Height = 400, 400
        self.Bodies = []
        self.Gravity = Vector(0.0, 9.81)

    def StepTime(self: World, time: float) -> None:
        self.Prerender(self)

        for body in self.Bodies:
            body.Step(time, self.Gravity)

        for i in range(len(self.Bodies)):
            bodyA = self.Bodies[i]
            for j in range(i + 1, len(self.Bodies)):
                bodyB = self.Bodies[j]
                collision = self.__Intersection(bodyA, bodyB)

                if collision:
                    self.OnCollide(bodyA, bodyB)

                    normal, depth = collision
                    bodyA.Move(normal * depth / 2.0)
                    bodyB.Move(-normal * depth / 2.0)
                    collisions.ResolveCollision(bodyA, bodyB, normal, depth)

    def GenerateFrame(self: World) -> Image.Image:
        img = Image.new('RGB', (self.Width, self.Height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        for body in self.Bodies:
            body.Draw(draw)

        return img

    def __Intersection(
        self: World, bodyA: BoxBody | CircleBody, bodyB: BoxBody | CircleBody
    ) -> tuple[Vector, float] | None:
        if isinstance(bodyA, BoxBody):
            if isinstance(bodyB, BoxBody):
                return collisions.Polygons(
                    bodyA.Position,
                    bodyA.GetTransformedVertices(),
                    bodyB.Position,
                    bodyB.GetTransformedVertices(),
                )
            else:
                return collisions.CirclePolygon(
                    bodyB.Position, bodyB.Radius, bodyA.Position, bodyA.GetTransformedVertices()
                )

        elif isinstance(bodyB, BoxBody):
            t = collisions.CirclePolygon(
                bodyA.Position, bodyA.Radius, bodyB.Position, bodyB.GetTransformedVertices()
            )

            if t:
                return -t[0], t[1]

        else:
            return collisions.Circle(bodyA.Position, bodyA.Radius, bodyB.Position, bodyB.Radius)

    # Arguments for this function are the same as the constructor for CircleBody class.
    def CreateCircleBody(self: World, *args) -> None:
        self.Bodies.append(CircleBody(*args))

    # Arguments for this function are the same as the constructor for BoxBody class.
    def CreateBoxBody(self: World, *args) -> None:
        self.Bodies.append(BoxBody(*args))
