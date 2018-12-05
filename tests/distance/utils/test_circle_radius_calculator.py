from unittest import TestCase
import cv2
import numpy as np
from parameterized import parameterized

from mrc.distance.utils.circle_radius_calculator import calculate_radius
from mrc.localization.color.utils.color_converter import ColorConverter
from tests.test_utils.read_image import read_image


class TestColorConverterGrayscale(TestCase):
    def setUp(self):
        self.converter = ColorConverter()
        self.images = [read_image('distance/utils/circle_radius/1.png'),
                       read_image('distance/utils/circle_radius/1t.png')]

    @parameterized.expand([[i] for i in range(2)])
    def test_calculate_radius(self, image_id):
        radius = calculate_radius(self.images[image_id])
        self.assertAlmostEqual(radius, 268, delta=3)
