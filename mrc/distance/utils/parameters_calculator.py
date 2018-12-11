import json
import math
from scipy.optimize import curve_fit

from mrc.distance.distance_function import distance_function_with_params
from mrc.localization.camera.utils.diode_detector import DiodeDetector
from mrc.localization.color.utils.color_converter import ColorConverter
from mrc.shared.exceptions.exceptions import DataSizeException
from mrc.utils.maths import normalize_point_in_circle, vector_2d_length


class CameraParametersCalculator:
    def __init__(self, photos, distances, height_difference, circle_radius, color_encoding='BGR'):
        if len(photos) != len(distances):
            raise DataSizeException
        self.color_converter = ColorConverter()
        self.photos = photos
        self.resolution = self.photos[0].shape[0:2]
        self.reality_distances = distances
        self.h = height_difference
        self.color_encoding = color_encoding
        self.diode_detector = DiodeDetector()
        self.circle_radius = circle_radius

    def calculate_parameters(self, filename=None):
        reality_angles = [math.atan(dist / self.h) for dist in self.reality_distances]
        diodes = [self.diode_detector.detect(p, color_encoding=self.color_encoding)[0][0].pt for p in self.photos]
        photo_normalized_distances = [
            vector_2d_length(normalize_point_in_circle(d, self.resolution, self.circle_radius)) for d in diodes]
        coef, _ = curve_fit(distance_function_with_params, photo_normalized_distances, reality_angles)
        if filename is not None:
            self._export_coef(coef, filename)
        return coef

    @staticmethod
    def _export_coef(coef, filename):
        coef_json = {'a': coef[0], 'b': coef[1], 'c': coef[2], 'd': coef[3]}
        with open(filename, 'w+') as file:
            json.dump(coef_json, file)
