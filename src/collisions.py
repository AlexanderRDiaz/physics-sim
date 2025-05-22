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


def ResolveBoxes(b1: Body, b2: Body) -> object:
    assert b1.ShapeType == Enums.ShapeType.Box, (
        'Body 1 is not a box, intersection cannot be resolved!'
    )
    assert b2.ShapeType == Enums.ShapeType.Box, (
        'Body 2 is not a box, intersection cannot be resolved!'
    )

    distances = +(b1.Position - b2.Position)
    xMin, yMin = b1.Width + b2.Width, b1.Height + b2.Height

    normal = Vector.Normal()


def ResolveBoxCircle(b1: Body, b2: Body):
    if b1.ShapeType == Enums.ShapeType.Circle and b2.ShapeType == Enums.ShapeType.Box:
        circle, box = b1, b2
    elif b1.ShapeType == Enums.ShapeType.Box and b2.ShapeType == Enums.ShapeType.Circle:
        circle, box = b2, b1
    else:
        raise RuntimeError(
            f'Cannot resolve for a box and circle with a {b1.ShapeType} and {b2.ShapeType}',
        )
