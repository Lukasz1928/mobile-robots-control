from unittest import TestCase

import cv2
from parameterized import parameterized

from mrc.localization.camera.utils.diode_detector import DiodeDetector
from mrc.utils.maths import point_in_rectangle
from tests.resources.localization.diode_detection.blobs.multiple_blobs.data import \
    expected_locations as expected_locations_multiple
from tests.resources.localization.diode_detection.blobs.single_blob.data import \
    expected_locations as expected_locations_single
from tests.resources.localization.diode_detection.components.blobs.multiple_blobs.data import \
    expected_locations_diodes
from tests.test_utils.list_utils import lists_almost_equal
from tests.test_utils.read_image import read_image


# class TestDiodeDetectorNoDiode(TestCase):
#     def setUp(self):
#         self.detector = DiodeDetector()
#         self.image = read_image('localization/diode_detection/blobs/no_blob/1.png')
#
#     def test_detect(self):
#         diodes, areas = self.detector.detect(self.image)
#         self.assertListEqual(diodes, [])
#         self.assertListEqual(areas, [])
#
#
# class TestDiodeDetectorSingleDiode(TestCase):
#     def setUp(self):
#         self.detector = DiodeDetector()
#         self.images = [read_image('localization/diode_detection/blobs/single_blob/{}.png'.format(i)) for i in
#                        range(1, 10)]
#         self.expected_locations = expected_locations_single
#
#     @parameterized.expand([[i] for i in range(9)])
#     def test_detect(self, image_id):
#         img = self.images[image_id]
#         diodes, areas = self.detector.detect(img)
#         is_diode_in_area = [point_in_rectangle(diode.pt, (area[cv2.CC_STAT_LEFT], area[cv2.CC_STAT_TOP]),
#                                                (area[cv2.CC_STAT_WIDTH], area[cv2.CC_STAT_HEIGHT])) for diode, area in
#                             zip(diodes, areas)]
#         self.assertListEqual([True for _ in range(len(is_diode_in_area))], is_diode_in_area)
#         self.assertEqual(len(diodes), 1)
#         self.assertAlmostEqual(diodes[0].pt[0], self.expected_locations[image_id][0], delta=4)
#         self.assertAlmostEqual(diodes[0].pt[1], self.expected_locations[image_id][1], delta=4)
#
#
# class TestDiodeDetectorSingleDiodeMultipleBlobs(TestCase):
#     def setUp(self):
#         self.detector = DiodeDetector()
#         self.images = [read_image('localization/diode_detection/blobs/multiple_blobs/{}.png'.format(i)) for i in
#                        range(1, 10)]
#         self.expected_locations = expected_locations_multiple
#
#     @parameterized.expand([[i] for i in range(9)])
#     def test_detect(self, image_id):
#         img = self.images[image_id]
#         diodes, areas = self.detector.detect(img)
#         is_diode_in_area = [point_in_rectangle(diode.pt, (area[cv2.CC_STAT_LEFT], area[cv2.CC_STAT_TOP]),
#                                                (area[cv2.CC_STAT_WIDTH], area[cv2.CC_STAT_HEIGHT])) for diode, area in
#                             zip(diodes, areas)]
#         self.assertListEqual([True for _ in range(len(is_diode_in_area))], is_diode_in_area)
#         self.assertEqual(len(diodes), 1)
#         self.assertAlmostEqual(diodes[0].pt[0], self.expected_locations[image_id][0], delta=4)
#         self.assertAlmostEqual(diodes[0].pt[1], self.expected_locations[image_id][1], delta=4)
#
#
# class TestDiodeDetectorMultipleDiodes(TestCase):
#     def setUp(self):
#         self.detector = DiodeDetector()
#         self.images = [read_image('localization/diode_detection/components/blobs/multiple_blobs/{}.png'.format(i)) for i
#                        in range(1, 3)]
#         self.expected_locations = expected_locations_diodes
#
#     @parameterized.expand([[i] for i in range(2)])
#     def test_detect_single_diode(self, image_id):
#         img = self.images[image_id]
#         diodes, areas = self.detector.detect(img)
#         is_diode_in_area = [point_in_rectangle(diode.pt, (area[cv2.CC_STAT_LEFT], area[cv2.CC_STAT_TOP]),
#                                                (area[cv2.CC_STAT_WIDTH], area[cv2.CC_STAT_HEIGHT])) for diode, area in
#                             zip(diodes, areas)]
#         self.assertListEqual([True for _ in range(len(is_diode_in_area))], is_diode_in_area)
#         self.assertEqual(len(diodes), len(self.expected_locations[image_id + 1]))
#         self.assertEqual(len(diodes), len(self.expected_locations[image_id + 1]))
#         self.assertTrue(
#             lists_almost_equal([(d.pt[0], d.pt[1]) for d in diodes], self.expected_locations[image_id + 1], 4))
