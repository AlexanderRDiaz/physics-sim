import sys

from .matrix import Vector


def ResolveCircles(
    positionA: Vector,
    positionB: Vector,
    radiusA: float,
    radiusB: float,
) -> tuple[Vector | None, float | None]:
    distance = positionA.Distance(positionB)
    radii = radiusA + radiusB

    if distance >= radii:
        return None, None

    return (positionB - positionA).Normal(), radii - distance


def ResolvePolygons(
    verticesA: list[Vector], verticesB: list[Vector]
) -> tuple[Vector | None, float | None]:
    normal = Vector.Zero()
    depth = -sys.float_info.max

    for i in range(len(verticesA)):
        va = verticesA[i]
        vb = verticesA[(i + 1) % len(verticesA)]

        edge = vb - va
        axis = Vector(-edge.Y, edge.X)

        minA, maxA = __ProjectVertices(verticesA, axis)
        minB, maxB = __ProjectVertices(verticesB, axis)

        if minA >= maxB or minB >= maxA:
            return None, None

        axisDepth = min(maxB - maxA, maxA - maxB)

        if axisDepth < depth:
            depth = axisDepth
            normal = axis

    for i in range(len(verticesB)):
        va = verticesB[i]
        vb = verticesB[(i + 1) % len(verticesB)]

        edge = vb - va
        axis = Vector(-edge.Y, edge.X)

        minA, maxA = __ProjectVertices(verticesA, axis)
        minB, maxB = __ProjectVertices(verticesB, axis)

        if minA >= maxB or minB >= maxA:
            return None, None

        axisDepth = min(maxB - maxA, maxA - maxB)

        if axisDepth < depth:
            depth = axisDepth
            normal = axis

    depth /= normal.Length()
    normal = normal.Normal()

    return normal, depth


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
