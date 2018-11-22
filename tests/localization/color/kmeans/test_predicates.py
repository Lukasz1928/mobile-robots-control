from unittest import TestCase

from parameterized import parameterized

from mrc.localization.color.kmeans.defaults import DefaultColorValues
from mrc.localization.color.kmeans.predicates import GaussianHSVPredicate
from tests.localization.color.kmeans import common


class TestGaussianHSVPredicate(TestCase):
    def setUp(self):
        self.gaussian_predicate = GaussianHSVPredicate()

    @parameterized.expand(zip(common.centroid_hsv_values, common.colors_analyzed))
    def test_call(self, a, b):
        hue, _, _ = a
        for name, value in b.items():
            _range = DefaultColorValues[name].value
            self.assertEqual(value, self.gaussian_predicate(hue, _range))
