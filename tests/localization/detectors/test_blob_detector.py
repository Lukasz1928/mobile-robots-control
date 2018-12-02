from unittest import TestCase
from parameterized import parameterized
from mrc.localization.camera.utils.blob_detector import BlobDetector
from mrc.localization.color.utils.color_converter import ColorConverter
from tests.resources.localization.diode_detection.blobs.multiple_blobs.expected_locations import \
    expected_locations as multiple_expected_locations
from tests.resources.localization.diode_detection.blobs.single_blob.expected_locations import \
    expected_locations as single_expected_locations
from tests.test_utils.read_image import read_image
from tests.test_utils.list_utils import list_contains_almost


class TestBlobDetectorNoBlob(TestCase):
    def setUp(self):
        self.detector = BlobDetector()
        self.color_converter = ColorConverter()
        self.image = self.color_converter.convert_to_grayscale(
            read_image('localization/diode_detection/blobs/no_blob/1.jpg'))

    def test_detect(self):
        blobs = self.detector.detect(self.image)
        self.assertListEqual(blobs, [])


class TestBlobDetectorSingleBlob(TestCase):
    def setUp(self):
        self.detector = BlobDetector(min_area=5)
        self.color_converter = ColorConverter()
        self.images = [self.color_converter.convert_to_grayscale(
            read_image('localization/diode_detection/blobs/single_blob/{}.jpg'.format(i))) for i in range(1, 10)]
        self.expected_locations = single_expected_locations

    @parameterized.expand([[i] for i in range(9)])
    def test_detect(self, image_id):
        img = self.images[image_id]
        blobs = self.detector.detect(img)
        self.assertEqual(len(blobs), 1)
        self.assertAlmostEqual(blobs[0].pt[0], self.expected_locations[image_id][0], delta=5)
        self.assertAlmostEqual(blobs[0].pt[1], self.expected_locations[image_id][1], delta=5)


class TestBlobDetectorMultipleBlobs(TestCase):
    def setUp(self):
        self.detector = BlobDetector(min_area=5)
        self.color_converter = ColorConverter()
        self.images = [self.color_converter.convert_to_grayscale(
            read_image('localization/diode_detection/blobs/multiple_blobs/{}.png'.format(i))) for i in range(1, 10)]
        self.expected_locations = multiple_expected_locations

    @parameterized.expand([[i] for i in range(9)])
    def test_detect(self, image_id):
        img = self.images[image_id]
        blobs = self.detector.detect(img)
        self.assertGreaterEqual(len(blobs), 1)
        self.assertTrue(list_contains_almost(self.expected_locations[image_id], [b.pt for b in blobs], 5))
