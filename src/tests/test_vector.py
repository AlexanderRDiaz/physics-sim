from __future__ import annotations

import math
import unittest

from src import testlib
from src.matrix import Vector


class Main(unittest.TestCase):
    def test_math(self: Main):
        a = Vector(2, 7)
        b = Vector(3, -5)

        sumVector = a + b
        self.assertTrue(sumVector.X == float(a.X + b.X) and sumVector.Y == float(a.Y + b.Y))

        diff1 = a - b
        self.assertTrue(diff1.X == float(a.X - b.X) and diff1.Y == float(a.Y - b.Y))
        diff2 = b - a
        self.assertTrue(diff2.X == float(b.X - a.X) and diff2.Y == float(b.Y - a.Y))

        product1 = b * -3
        self.assertTrue(product1.X == float(b.X * -3) and product1.Y == float(b.Y * -3))
        product2 = b * 2
        self.assertTrue(product2.X == float(b.X * 2) and product2.Y == float(b.Y * 2))

        quotient1 = b / 2
        self.assertTrue(quotient1.X == float(b.X / 2) and quotient1.Y == float(b.Y / 2))

        floorquo1 = b // 2
        self.assertTrue(floorquo1.X == float(b.X // 2) and floorquo1.Y == float(b.Y // 2))

        negated = -b
        self.assertTrue(negated.X == float(-b.X) and negated.Y == float(-b.Y))

    def test_compare(self: Main):
        i = Vector(100, 100)
        f = Vector(100.0, 100.0)
        z = Vector.Zero()

        self.assertFalse(i == 0)
        self.assertTrue(i != 0)

        self.assertTrue(i == f)
        self.assertFalse(i != f)

        self.assertTrue(i != z)
        self.assertFalse(f == z)

    def test_lib(self: Main):
        a = Vector(2, 2)
        b = Vector(3, 5)

        length = b.Length()
        self.assertTrue(length == math.sqrt(b.X**2 + b.Y**2))
        normal = b.Normal()
        self.assertTrue(normal.X == (b.X / length) and normal.Y == (b.Y / length))
        distance = a.Distance(b)
        self.assertTrue(distance == math.sqrt((a.X - b.X) ** 2 + (a.Y - b.Y) ** 2))
        dot = a.Dot(b)
        self.assertTrue(dot == (a.X * b.X) + (a.Y * b.Y))
        cross = a.Cross(b)
        self.assertTrue(cross == (a.X * b.Y) - (a.Y * b.X))


if __name__ == '__main__':
    testlib.SoloRunOutput(__file__)
    unittest.main()
