import math
from unittest import TestCase

import numpy as np
from parameterized import parameterized
from numpy.testing import assert_almost_equal
from mrc.utils.maths import gauss_distribution, points_2d_distance, vector_2d_length, rescale_rectangle, \
    normalize_point_in_circle


class TestGaussDistribution(TestCase):

    @parameterized.expand([[mu, std] for mu in np.linspace(-2, 2, 3) for std in np.linspace(1, 2, 3)])
    def test_max_value_location(self, mu, stdev):
        xs = np.linspace(mu - 3 * stdev, mu + 3 * stdev, 250)
        ys = [gauss_distribution(x, mu, stdev) for x in xs]
        self.assertAlmostEqual(ys.index(max(ys)), len(ys) // 2, delta=3)


class TestPointsDistance(TestCase):
    def setUp(self):
        self.points = [(0, 0), (1, 0), (2, 1), (1, 3)]
        self.distances = [[0, 1, math.sqrt(5), math.sqrt(10)],
                          [1, 0, math.sqrt(2), 3],
                          [math.sqrt(5), math.sqrt(2), 0, math.sqrt(5)],
                          [math.sqrt(10), 3, math.sqrt(5), 0]]

    @parameterized.expand([[i, j] for i in range(4) for j in range(4)])
    def test_distance(self, i, j):
        self.assertAlmostEqual(points_2d_distance(self.points[i], self.points[j]), self.distances[i][j], 3)


class TestVectorLength(TestCase):
    def setUp(self):
        self.vectors = [(0, 0), (1, 0), (2, 1), (1, 3)]
        self.lengths = [0, 1, math.sqrt(5), math.sqrt(10)]

    @parameterized.expand([[i] for i in range(4)])
    def test_lengths(self, i):
        self.assertAlmostEqual(vector_2d_length(self.vectors[i]), self.lengths[i])


class TestRescaleRectangle(TestCase):
    def setUp(self):
        self.rectangle = [(-1, -1), (2, 2)]
        self.ratios = [0.5, 1, 2]
        self.expected = [[(-0.5, -0.5), (1, 1)],
                         [(-1, -1), (2, 2)],
                         [(-2, -2), (4, 4)]]

    @parameterized.expand([[r] for r in [0.5, 1, 2]])
    def test_simple_rescale(self, ratio):
        rescaled = rescale_rectangle(self.rectangle[0], self.rectangle[1], ratio)
        assert_almost_equal(rescaled[0], self.expected[self.ratios.index(ratio)][0])
        assert_almost_equal(rescaled[1], self.expected[self.ratios.index(ratio)][1])

    def test_rescale(self):
        top_left = (0, 0)
        sides = (1, 1)
        rescaled = rescale_rectangle(top_left, sides, 2)
        expected_top_left = (-0.5, -0.5)
        expected_sides = (2, 2)
        assert_almost_equal(rescaled[0], expected_top_left)
        assert_almost_equal(rescaled[1], expected_sides)


class TestNormalizePoint(TestCase):
    def setUp(self):
        self.points = [(0, 0), (0, 50), (0, 100), (50, 0), (50, 50), (50, 100), (100, 0), (100, 50), (100, 100),
                       (50 + 50 / math.sqrt(2), 50 + 50 / math.sqrt(2)), (25, 25)]
        self.expected_locations = [(1, -1), (0, -1), (-1, -1), (1, 0), (0, 0), (-1, 0), (1, 1), (0, 1), (-1, 1),
                                   (-1 / math.sqrt(2), 1 / math.sqrt(2)), (0.5, -0.5)]
        self.resolution = (100, 100)
        self.radius = 50

    @parameterized.expand([[i] for i in range(9)])
    def test_normalize(self, i):
        normalized = normalize_point_in_circle(self.points[i], self.resolution, 50)
        assert_almost_equal(normalized, self.expected_locations[i])
