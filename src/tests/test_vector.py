from __future__ import annotations

import math
import unittest

from src import testlib
from src.matrix import Vector


class Main(unittest.TestCase):
    def test_math(self: Main):
        a = Vector(2.0, 7.0)
        b = Vector(3.0, -5.0)

        sumVector = a + b
        self.assertTrue(sumVector.X == (a.X + b.X) and sumVector.Y == (a.Y + b.Y))

        diff1 = a - b
        self.assertTrue(diff1.X == (a.X - b.X) and diff1.Y == (a.Y - b.Y))
        diff2 = b - a
        self.assertTrue(diff2.X == (b.X - a.X) and diff2.Y == (b.Y - a.Y))

        product1 = b * -3.0
        self.assertTrue(product1.X == (b.X * -3) and product1.Y == (b.Y * -3))
        product2 = b * 2.0
        self.assertTrue(product2.X == (b.X * 2) and product2.Y == (b.Y * 2))

        quotient1 = b / 2.0
        self.assertTrue(quotient1.X == (b.X / 2) and quotient1.Y == (b.Y / 2))

        floorquo1 = b // 2.0
        self.assertTrue(floorquo1.X == (b.X // 2.0) and floorquo1.Y == (b.Y // 2.0))

        negated = -b
        self.assertTrue(negated.X == (-b.X) and negated.Y == (-b.Y))

    def test_compare(self: Main):
        f = Vector(100.0, 100.0)
        z = Vector.Zero()

        self.assertFalse(f == 0.0)
        self.assertTrue(f != 0.0)

        self.assertTrue(f != z)
        self.assertFalse(f == z)

    def test_lib(self: Main):
        a = Vector(2.0, 2.0)
        b = Vector(3.0, 5.0)

        length = b.Length()
        self.assertTrue(length == math.sqrt(b.X**2.0 + b.Y**2.0))
        normal = b.Normal()
        self.assertTrue(normal.X == (b.X / length) and normal.Y == (b.Y / length))
        distance = a.Distance(b)
        self.assertTrue(distance == math.sqrt((a.X - b.X) ** 2.0 + (a.Y - b.Y) ** 2.0))
        dot = a.Dot(b)
        self.assertTrue(dot == (a.X * b.X) + (a.Y * b.Y))
        cross = a.Cross(b)
        self.assertTrue(cross == (a.X * b.Y) - (a.Y * b.X))


if __name__ == '__main__':
    testlib.SoloRunOutput(__file__)
    unittest.main()
