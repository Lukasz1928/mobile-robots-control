import math

from mrc.localization.calculator.abstract_calculator import AbstractLocationCalculator
from mrc.utils.maths import vector_2d_length, normalize_point_in_circle


class LocationCalculator(AbstractLocationCalculator):
    def __init__(self, resolution, distance_function, circle_radius, angle_function=None):
        self.resolution = resolution
        self.image_circle_radius = circle_radius
        self.distance_function = distance_function
        self.angle_function = angle_function

    def calculate_location(self, point):
        norm_point = normalize_point_in_circle(point, self.resolution, self.image_circle_radius)
        return self._calculate_distance(norm_point), self._calculate_angle(norm_point)

    def _calculate_distance(self, normalized_point):
        return self.distance_function(vector_2d_length(normalized_point))

    def _calculate_angle(self, point):
        if self.angle_function is not None:
            return self.angle_function(point)
        if point[0] == 0 and point[1] == 0:
            return 0.0
        return math.atan2(point[1], point[0])
