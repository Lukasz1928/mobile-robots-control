from unittest import TestCase

from mrc.localization.color.kmeans.kmeans_strategy import KMeansStrategy
from tests.localization.color.kmeans import common


class TestKMeansStrategy(TestCase):
    def setUp(self):
        self.kmeans_strategy = KMeansStrategy()

    def test_call(self):
        expected_extracted = ['green', 'red', 'green', 'yellow', 'red', 'red']
        actual_extracted = self.kmeans_strategy(common.image, common.blob_coordinates)
        self.assertEqual(expected_extracted, actual_extracted)
