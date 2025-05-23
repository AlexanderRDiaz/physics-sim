from body import Body
from matrix import Vector

import enums as Enums


def ResolveCircles(c1: Body, c2: Body) -> tuple[Vector, float]:
    assert c1.ShapeType == Enums.ShapeType.Circle, (
        'Body 1 is not a circle, intersection cannot be resolved!'
    )
    assert c2.ShapeType == Enums.ShapeType.Circle, (
        'Body 2 is not a circle, intersection cannot be resolved!'
    )

    distance = Vector.Distance(c1.Position, c2.Position)
    radii = c1.Radius + c2.Radius

    return Vector.Normal(c2.Position - c1.Position), radii - distance
