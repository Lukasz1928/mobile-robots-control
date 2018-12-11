import math

from mrc.distance.distance_function import get_distance_function_from_file
from mrc.localization.calculator.abstract_calculator import AbstractLocationCalculator
from mrc.shared.exceptions.exceptions import ParameterException
from mrc.utils.maths import vector_2d_length, normalize_point_in_circle


class LocationCalculator(AbstractLocationCalculator):
    def __init__(self, resolution, circle_radius, distance_function=None, angle_function=None, filename=None):
        self.resolution = resolution
        self.image_circle_radius = circle_radius
        if (distance_function is not None and filename is not None) or (distance_function is None and filename is None):
            raise ParameterException("Exactly one of [distance_function, filename] parameters must be set")
        if distance_function is not None:
            self.distance_function = distance_function
        else:
            self.distance_function = get_distance_function_from_file(filename)
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
