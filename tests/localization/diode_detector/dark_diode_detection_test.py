from unittest import TestCase
from parameterized import parameterized
from mrc.localization.camera.utils.diode_detector import DiodeDetector
from tests.resources.localization.diode_detector.expected_locations import expected_locations
from tests.test_utils.read_image import read_image


class TestDiodeDetectorNoDiode(TestCase):
    def setUp(self):
        self.detector = DiodeDetector()
        self.image = read_image('no_diode')

    def test_detect(self):
        keypoints = self.detector.detect(self.image)
        self.assertListEqual(keypoints, [])


class TestDiodeDetectorSingleDiode(TestCase):
    def setUp(self):
        self.detector = DiodeDetector()
        self.images = [read_image(i) for i in range(1, 10)]
        self.expected_locations = expected_locations

    @parameterized.expand([[i] for i in range(9)])
    def test_detect(self, image_id):
        img = self.images[image_id]
        keypoints = self.detector.detect(img)
        self.assertEqual(len(keypoints), 1)
        self.assertAlmostEqual(keypoints[0].pt[0], self.expected_locations[image_id][0], delta=3)
        self.assertAlmostEqual(keypoints[0].pt[1], self.expected_locations[image_id][1], delta=3)

