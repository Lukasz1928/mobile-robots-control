import math
from unittest import TestCase

from numpy.testing import assert_almost_equal
from parameterized import parameterized

from mrc.localization.position.probability import AngularProbability


class TestAngularProbablity(TestCase):

    def setUp(self):
        self.angular_prob = AngularProbability(2 * math.pi / 10, 0, 3)

    def test_calling(self):
        assert_almost_equal(self.angular_prob(-math.pi), self.angular_prob(math.pi), 5)
        assert_almost_equal(3 * self.angular_prob(-math.pi) / 2, self.angular_prob(math.pi), 5)

    @parameterized.expand([[5], [3.14], [10], [27], [-0.1]])
    def test_shifting(self, shift_angle):
        self.angular_prob.shift(shift_angle)
        assert_almost_equal(self.angular_prob(self.angular_prob.mean + 0.5),
                            self.angular_prob(self.angular_prob.mean - 0.5), 3)
