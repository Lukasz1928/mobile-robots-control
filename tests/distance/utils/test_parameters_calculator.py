import math
from unittest import TestCase
from parameterized import parameterized
from mrc.distance.distance_function import get_distance_function
from mrc.distance.utils.parameters_calculator import CameraParametersCalculator
from mrc.localization.camera.utils.diode_detector import DiodeDetector
from mrc.localization.color.utils.color_converter import ColorConverter
from mrc.utils.maths import normalize_point_in_circle, vector_2d_length
from tests.test_utils.read_image import read_image
from tests.resources.distance.utils.parameters.data import expected_locations, image_circle_radius, height


class TestCameraParametersCalculator(TestCase):
    def setUp(self):
        self.converter = ColorConverter()
        self.images = [read_image('localization/diode_detection/blobs/single_blob/{}.png'.format(i)) for i in
                       range(1, 10)]
        self.diode_detector = DiodeDetector()
        self.radius = image_circle_radius
        self.calculator = CameraParametersCalculator(self.images, expected_locations, height, self.radius)
        self.parameters = self.calculator.calculate_parameters()
        self.function = get_distance_function(self.parameters)

    @parameterized.expand([[i] for i in range(9)])
    def test_calculate_radius(self, image_id):
        diodes, _ = self.diode_detector.detect(self.images[image_id])
        angle = self.function(
            vector_2d_length(normalize_point_in_circle(diodes[0].pt, self.images[image_id].shape[0:2], self.radius)))
        distance = math.tan(angle) * height
        self.assertAlmostEqual(distance, expected_locations[image_id], delta=6)
