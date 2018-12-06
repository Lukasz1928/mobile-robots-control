from enum import Enum
from unittest import TestCase

import cv2
from parameterized import parameterized

from mrc.localization.color.defaults import DefaultColorValues
from mrc.localization.color.quick_mean.quick_mean import Analyser
from tests.localization.color.quick_mean import common


class CustomColorValue(Enum):
    one = range(0, 40)
    two = range(41, 135)


class TestAnalyser(TestCase):
    @parameterized.expand(common.indexed_photos_with_colors)
    def test_analyse_chunk_with_default_colors(self, image, idx):
        analyser = Analyser(DefaultColorValues)

        estimated = analyser.analyse_chunk(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        self.assertEqual(estimated, common.colors_analyzed[idx])
