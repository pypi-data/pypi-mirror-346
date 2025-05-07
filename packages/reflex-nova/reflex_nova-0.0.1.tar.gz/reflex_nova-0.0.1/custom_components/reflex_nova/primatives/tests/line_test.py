import unittest

from reflex_nova.primatives.line import Line
from reflex_nova.primatives.point import Point
from reflex_nova.primatives.vector import Vector


class TestLine(unittest.TestCase):
    def test_parallel_lines_no_intersection(self):
        l1 = Line(Point(0, 0), Vector(1, 1))
        l2 = Line(Point(10, 10), Vector(1, 1))
        self.assertIsNone(l1.intersection_with(l2))

    def test_lines_intersection(self):
        l1 = Line(Point(50, 0), Vector(0, 1))
        l2 = Line(Point(0, 30), Vector(1, 0))
        actual = l1.intersection_with(l2)
        expected = Point(50, 30)
        self.assertEqual(expected, actual)
