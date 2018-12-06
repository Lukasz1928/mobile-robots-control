from unittest import TestCase
from unittest.mock import Mock

from parameterized import parameterized

from mrc.localization.color.quick_mean.quick_mean import Extractor

from tests.localization.color.quick_mean import common
from tests.test_utils.read_image import read_image


class TestExtractor(TestCase):

    def setUp(self):
        self.analyser_mock = Mock()
        self.extractor = Extractor(analyser=self.analyser_mock)

    @parameterized.expand(common.indexed_photos_with_colors)
    def test_extract(self, image, color, idx):
        self.analyser_mock.analyse_chunk.return_value = common.colors_analyzed[idx]
        actual_extracted = self.extractor.extract(image)
        self.analyser_mock.analyse_chunk.assert_called()
        self.assertEqual(color, actual_extracted)
