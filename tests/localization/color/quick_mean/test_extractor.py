from unittest import TestCase
from unittest.mock import Mock

from parameterized import parameterized

from mrc.localization.color.quick_mean.quick_mean import ColorCalculator
from tests.localization.color.quick_mean import common


class TestColorCalculator(TestCase):

    def setUp(self):
        self.analyser_mock = Mock()
        self.extractor = ColorCalculator(analyser=self.analyser_mock)

    @parameterized.expand(common.indexed_photos_with_colors)
    def test_extract(self, image, color, idx):
        self.analyser_mock.analyse_chunk.return_value = common.colors_analyzed[idx]
        actual_extracted = self.extractor.extract(image)
        self.analyser_mock.analyse_chunk.assert_called()
        self.assertEqual(color, actual_extracted)
