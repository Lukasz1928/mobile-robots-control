from unittest import TestCase
from parameterized import parameterized
from mrc.distance.utils.circle_radius_calculator import calculate_radius
from mrc.localization.color.utils.color_converter import ColorConverter
from tests.test_utils.read_image import read_image


class TestColorConverterGrayscale(TestCase):
    def setUp(self):
        self.converter = ColorConverter()
        self.images = [read_image('distance/utils/circle_radius/1.png'),
                       read_image('distance/utils/circle_radius/1t.png')]
        self.expected_radius = [268, 268]

    @parameterized.expand([[i] for i in range(2)])
    def test_calculate_radius(self, image_id):
        radius = calculate_radius(self.images[image_id])
        self.assertAlmostEqual(radius, self.expected_radius[image_id], delta=3)
