from unittest import TestCase

import numpy as np
from parameterized import parameterized

from mrc.localization.color.kmeans.utils import hsv_pixel_from_centroid, rgb2hsv
from tests.localization.color.kmeans import common


class TestUtils(TestCase):
    @parameterized.expand(zip(common.centroid_rgb_values, common.centroid_hsv_values))
    def test_hsv_pixel_from_centroid(self, float_rgb_values, expected_values):
        self.assertEqual(expected_values, hsv_pixel_from_centroid(np.asarray(float_rgb_values)))

    @parameterized.expand(zip(common.centroid_rgb_values, common.centroid_hsv_values))
    def test_rgb2hsv(self, float_rgb_values, expected_values):
        int_rgb_values = np.asarray(float_rgb_values).astype('uint8').reshape(1, 3)[0]
        self.assertEqual(expected_values, rgb2hsv(*int_rgb_values))
