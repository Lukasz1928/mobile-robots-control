from unittest import TestCase
from unittest.mock import Mock

from mrc.localization.color.kmeans.extractor import Extractor
from tests.localization.color.kmeans import common


class TestExtractor(TestCase):
    def setUp(self):
        self.analyser_mock = Mock()
        self.extractor = Extractor(analyser=self.analyser_mock)

    def test_extract(self):
        self.analyser_mock.analyse_chunk.side_effect = common.colors_analyzed
        expected_extracted = ['green', 'red', 'green', 'yellow', 'red', 'red']
        actual_extracted = self.extractor.extract(image=common.image, blob_coordinates=common.blob_coordinates)
        self.analyser_mock.analyse_chunk.assert_called()
        self.assertEqual(expected_extracted, actual_extracted)
