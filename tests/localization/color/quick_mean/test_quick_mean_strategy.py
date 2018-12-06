from unittest import TestCase

from parameterized import parameterized

from mrc.localization.color.quick_mean.quick_mean import QuickMeanStrategy
from tests.localization.color.quick_mean import common


class TestKMeansStrategy(TestCase):
    def setUp(self):
        self.quick_mean_strategy = QuickMeanStrategy()

    @parameterized.expand(common.photos_with_colors)
    def test_call(self, image, color):
        actual_extracted = self.quick_mean_strategy(image)
        self.assertEqual(color, actual_extracted)
