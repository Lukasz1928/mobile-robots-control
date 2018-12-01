import math
from unittest import TestCase

import numpy as np
from numpy.testing import assert_almost_equal
from parameterized import parameterized

from mrc.localization.position.probability import AngularProbability


class TestAngularProbability(TestCase):

    def setUp(self):
        self.angular_prob = AngularProbability(2 * math.pi / 10, 0, 3)

    @parameterized.expand([[5], [3.14], [10], [27], [-0.1]])
    def test_shifting(self, shift_angle):
        self.angular_prob.shift(shift_angle)
        assert_almost_equal(self.angular_prob(self.angular_prob.mean + 0.5),
                            self.angular_prob(self.angular_prob.mean - 0.5), 3)

    def test_calling_in_range(self):
        assert_almost_equal(self.angular_prob(-math.pi), self.angular_prob(math.pi), 3)

    def test_calling_out_of_range(self):
        assert_almost_equal(self.angular_prob(3 * -math.pi), self.angular_prob(math.pi), 3)

    @parameterized.expand([[i] for i in np.linspace(-math.pi, math.pi, 10)])
    def test_shifting_for_real_cases(self, shift_angle):
        self.angular_prob.shift(shift_angle)
        assert_almost_equal(self.angular_prob(self.angular_prob.mean + 0.5),
                            self.angular_prob(self.angular_prob.mean - 0.5), 3)

    def test_over_range(self):
        self.angular_prob.shift(math.pi)
        assert_almost_equal(self.angular_prob(self.angular_prob.mean + 0.5),
                            self.angular_prob(self.angular_prob.mean - 0.5), 3)
