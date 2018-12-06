from functools import reduce

import cv2
import numpy as np

from mrc.localization.color.abstract import ColorRecognitionStrategy
from mrc.localization.color.defaults import DefaultColorValues
from mrc.localization.color.quick_mean.predicates import GaussianHSVPredicate
from mrc.localization.color.utils.color_converter import rgb2hsv


class QuickMeanStrategy(ColorRecognitionStrategy):
    def __init__(self, color_values=DefaultColorValues, fitting_strategy='gaussian'):
        self.analyser = ColorAnalyser(predicate_strategy=fitting_strategy, color_values=color_values)
        self.extractor = ColorCalculator(self.analyser)

    def __call__(self, image):
        return self.extractor.extract(image)


class Predicates:
    allowed = {
        'gaussian': GaussianHSVPredicate()
    }


class ColorAnalyser:
    def __init__(self, color_values, predicate_strategy='gaussian'):
        self._resolving_predicate = Predicates.allowed[predicate_strategy]
        self._color_values = color_values

    def analyse_chunk(self, image_chunk):
        pixel_list = image_chunk.reshape(-1, 3)
        mean_color = np.mean(pixel_list, axis=0)
        return self._color_analysis(rgb2hsv(*mean_color))

    def _color_analysis(self, hsv_pixel):
        hue, _, _ = hsv_pixel
        return {color_val.name: self._resolving_predicate(hue, color_val.value) for color_val in
                self._color_values}


class ColorCalculator:
    def __init__(self, analyser):
        self.analyser = analyser

    def extract(self, image):
        _image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self._execute_analysis(_image)

    def _execute_analysis(self, chunk):
        analysis = self.analyser.analyse_chunk(chunk)
        return reduce(lambda i1, i2: max(i1, i2, key=lambda x: x[1]), analysis.items())[0]