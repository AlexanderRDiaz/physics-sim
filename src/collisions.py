import sys

from .body import BoxBody, CircleBody
from .matrix import Vector


def ResolveCollision(
    bodyA: BoxBody | CircleBody, bodyB: BoxBody | CircleBody, normal: Vector, depth: float
) -> None:
    relativeVelocity = bodyB.LinearVelocity - bodyA.LinearVelocity

    if relativeVelocity.Dot(normal) > 0:
        return

    e = min(bodyA.Restitution, bodyB.Restitution)

    j = -(1.0 + e) * relativeVelocity.Dot(normal)
    j /= bodyA.InverseMass + bodyB.InverseMass
    impulse = normal * j

    bodyA.LinearVelocity += impulse * bodyA.InverseMass
    bodyB.LinearVelocity -= impulse * bodyB.InverseMass


def CirclePolygon(
    circleCenter: Vector,
    radius: float,
    polygonCenter: Vector,
    vertices: tuple[Vector, ...],
) -> tuple[Vector, float] | None:
    normal = Vector.Zero()
    depth = sys.float_info.max

    for i in range(len(vertices)):
        a = vertices[i]
        b = vertices[(i + 1) % len(vertices)]

        edge = b - a
        axis = Vector(-edge.Y, edge.X).Normal()

        minA, maxA = __ProjectVertices(vertices, axis)
        minB, maxB = __ProjectCircle(circleCenter, radius, axis)

        if minA >= maxB or minB >= maxA:
            return

        axisDepth = min(maxB - minA, maxA - minB)

        if axisDepth < depth:
            depth = axisDepth
            normal = axis

    closest = __ClosestPointOnPolygon(circleCenter, vertices)

    axis = (closest - circleCenter).Normal()

    minA, maxA = __ProjectVertices(vertices, axis)
    minB, maxB = __ProjectCircle(circleCenter, radius, axis)

    if minA >= maxB or minB >= maxA:
        return

    axisDepth = min(maxB - minA, maxA - minB)

    if axisDepth < depth:
        depth = axisDepth
        normal = axis

    direction = circleCenter - polygonCenter

    if direction.Dot(normal) < 0.0:
        normal = -normal

    return normal, depth


def Circle(
    centerA: Vector, radiusA: float, centerB: Vector, radiusB: float
) -> tuple[Vector, float] | None:
    distance = centerA.Distance(centerB)
    radii = radiusA + radiusB

    if distance >= radii:
        return

    return (centerA - centerB).Normal(), radii - distance


def Polygons(
    centerA: Vector, verticesA: tuple[Vector, ...], centerB: Vector, verticesB: tuple[Vector, ...]
) -> tuple[Vector, float] | None:
    normal = Vector.Zero()
    depth = sys.float_info.max

    for i in range(len(verticesA)):
        a = verticesA[i]
        b = verticesA[(i + 1) % len(verticesA)]

        edge = b - a
        axis = Vector(-edge.Y, edge.X).Normal()

        minA, maxA = __ProjectVertices(verticesA, axis)
        minB, maxB = __ProjectVertices(verticesB, axis)

        if minA >= maxB or minB >= maxA:
            return

        axisDepth = min(maxB - minA, maxA - minB)

        if axisDepth < depth:
            depth = axisDepth
            normal = axis

    for i in range(len(verticesB)):
        a = verticesB[i]
        b = verticesB[(i + 1) % len(verticesB)]

        edge = b - a
        axis = Vector(-edge.Y, edge.X).Normal()

        minA, maxA = __ProjectVertices(verticesA, axis)
        minB, maxB = __ProjectVertices(verticesB, axis)

        if minA >= maxB or minB >= maxA:
            return

        axisDepth = min(maxB - minA, maxA - minB)

        if axisDepth < depth:
            depth = axisDepth
            normal = axis

    direction = centerA - centerB

    if direction.Dot(normal) < 0.0:
        normal = -normal

    return normal, depth


def __ClosestPointOnPolygon(center: Vector, vertices: tuple[Vector, ...]) -> Vector:
    result = -1
    minDistance = sys.float_info.max

    for i, v in enumerate(vertices):
        distance = center.Distance(v)

        if distance < minDistance:
            minDistance = distance
            result = i

    return vertices[result]


def __ProjectCircle(center: Vector, radius: float, axis: Vector) -> tuple[float, float]:
    direction = axis.Normal()
    directionRadius = direction * radius

    a = center + directionRadius
    b = center - directionRadius

    minimum = a.Dot(axis)
    maximum = b.Dot(axis)

    if maximum < minimum:
        minimum, maximum = maximum, minimum

    return minimum, maximum


def __ProjectVertices(vertices: tuple[Vector, ...], axis: Vector) -> tuple[float, float]:
    minimum = sys.float_info.max
    maximum = -sys.float_info.max

    for v in vertices:
        p = v.Dot(axis)
        minimum = min(minimum, p)
        maximum = max(maximum, p)

    return minimum, maximum
