import sys

from .matrix import Vector


def ResolveCircles(
    positionA: Vector,
    positionB: Vector,
    radiusA: float,
    radiusB: float,
) -> tuple[Vector, float]:
    distance = Vector.Distance(positionA, positionB)
    radii = radiusA + radiusB

    return Vector.Normal(positionB - positionA), radii - distance


def ResolvePolygons(verticesA: list[Vector], verticesB: list[Vector]) -> bool:
    for i in range(len(verticesA)):
        va = verticesA[i]
        vb = verticesA[(i + 1) % len(verticesA)]

        edge = vb - va
        axis = Vector(-edge.Y, edge.X)

        minA, maxA = __ProjectVertices(verticesA, axis)
        minB, maxB = __ProjectVertices(verticesB, axis)

        if minA >= maxB or minB >= maxA:
            return False

    for i in range(len(verticesB)):
        va = verticesB[i]
        vb = verticesB[(i + 1) % len(verticesB)]

        edge = vb - va
        axis = Vector(-edge.Y, edge.X)

        minA, maxA = __ProjectVertices(verticesA, axis)
        minB, maxB = __ProjectVertices(verticesB, axis)

        if minA >= maxB or minB >= maxA:
            return False

    return True


def __ProjectVertices(vertices: list[Vector], axis: Vector) -> tuple[float, float]:
    minimum = -sys.float_info.max
    maximum = sys.float_info.min

    for v in vertices:
        p = Vector.Dot(v, axis)

        if p < minimum:
            minimum = p
        elif p > maximum:
            maximum = p

    return minimum, maximum
