from enum import Enum
from unittest import TestCase

from mrc.localization.color.kmeans.analyser import Analyser
from mrc.localization.color.kmeans.defaults import DefaultColorValues
from tests.localization.color.kmeans import common


class CustomColorValue(Enum):
    one = range(0, 40)
    two = range(41, 135)


class TestAnalyser(TestCase):
    def test_analyse_chunk_with_default_colors(self):
        analyser = Analyser(color_values=DefaultColorValues)
        colors_found = list(analyser.analyse_chunk(common.image).keys())
        self.assertEqual(DefaultColorValues.red.name, colors_found[0])
        self.assertEqual(DefaultColorValues.yellow.name, colors_found[1])
        self.assertEqual(DefaultColorValues.green.name, colors_found[2])

    def test_analyse_chunk_with_custom_colors(self):
        analyser = Analyser(color_values=CustomColorValue)
        colors_found = list(analyser.analyse_chunk(common.image).keys())
        self.assertEqual(CustomColorValue.one.name, colors_found[0])
        self.assertEqual(CustomColorValue.two.name, colors_found[1])
