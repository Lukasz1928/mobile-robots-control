from unittest import TestCase

from parameterized import parameterized

from mrc.localization.color.quick_mean.quick_mean import QuickMeanStrategy
from tests.test_utils.read_image import read_image


class TestKMeansStrategy(TestCase):
    def setUp(self):
        self.quick_mean_strategy = QuickMeanStrategy()

    @parameterized.expand([
        (read_image('localization/color/quick_mean/{}.png'.format(i)), i)
        for i in ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']])
    def test_call(self, image, color):
        actual_extracted = self.quick_mean_strategy(image)
        self.assertEqual(color, actual_extracted)
