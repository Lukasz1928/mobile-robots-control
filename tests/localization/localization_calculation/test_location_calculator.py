import math
from unittest import TestCase
from unittest.mock import Mock

from parameterized import parameterized

from mrc.localization.location_calculator import LocationCalculator


class LocationCalculatorTest(TestCase):
    def setUp(self):
        self.locations_in_photos = [(50, 50), (0, 50), (50, 0), (50, 100), (100, 50),
                                    (50 + 50 / math.sqrt(2), 50 + 50 / math.sqrt(2)), (25, 25)]
        self.distances_in_photo = [0, 1, 1, 1, 1, 1, 1 / math.sqrt(2)]
        self.expected_angles = [0, 0, -math.pi / 2.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 4.0, -math.pi / 4.0]
        self.circle_radius = 50
        self.resolution = (100, 100)
        self.distance_function = lambda x: x + 1  # Any arbitrary bijective function
        self.expected_distances = [self.distance_function(d) for d in self.distances_in_photo]
        self.calculator = LocationCalculator(self.resolution, self.distance_function, self.circle_radius)
        self.angle_function_mock = Mock(name='angle')
        self.custom_calculator = LocationCalculator(self.resolution, self.distance_function, self.circle_radius,
                                                    self.angle_function_mock)

    @parameterized.expand([[i] for i in range(7)])
    def test_distance(self, id):
        d, _ = self.calculator.calculate_location(self.locations_in_photos[id])
        self.assertAlmostEqual(d, self.expected_distances[id], places=4)

    @parameterized.expand([[i] for i in range(7)])
    def test_angle(self, id):
        _, a = self.calculator.calculate_location(self.locations_in_photos[id])
        self.assertAlmostEqual(a, self.expected_angles[id], places=4)

    def test_custom_angle_function(self):
        d, a = self.custom_calculator.calculate_location(self.locations_in_photos[0])
        self.angle_function_mock.assert_called_once()
