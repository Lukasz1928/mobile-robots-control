from unittest import TestCase

from parameterized import parameterized

from mrc.localization.color.utils.utils import rgb2hsv
from tests.localization.color.quick_mean import common


class TestUtils(TestCase):

    @parameterized.expand(zip(common.rgb_pixels, common.hsv_pixels))
    def test_rgb2hsv(self, float_rgb_values, expected_values):
        self.assertEqual(expected_values, rgb2hsv(*float_rgb_values))
