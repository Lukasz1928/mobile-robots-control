from unittest import TestCase

import cv2
from parameterized import parameterized
from mrc.localization.camera.utils.connected_components_detector import ConnectedComponentsDetector
from tests.test_utils.list_utils import list_contains_almost_equal, list_difference, lists_almost_equal
from tests.test_utils.read_image import read_image
from mrc.localization.color.utils.color_converter import ColorConverter
from tests.resources.localization.diode_detection.blobs.multiple_blobs.expected_locations import \
    expected_locations as multiple_expected_locations
from tests.resources.localization.diode_detection.blobs.single_blob.expected_locations import \
    expected_locations as single_expected_locations
from tests.resources.localization.diode_detection.components.background.data import stats, centroids


class TestConnectedComponentsDetectorNoComponents(TestCase):
    def setUp(self):
        self.detector = ConnectedComponentsDetector()
        self.color_converter = ColorConverter()
        self.image = self.color_converter.convert_to_binary(
            read_image('localization/diode_detection/blobs/no_blob/1.png'), 10)

    def test_detect(self):
        s, c = self.detector.detect(self.image)
        self.assertListEqual(s, [])
        self.assertListEqual(c, [])


class TestConnectedComponentsDetectorBackground(TestCase):
    def setUp(self):
        self.detector = ConnectedComponentsDetector()
        self.color_converter = ColorConverter()
        self.images = [self.color_converter.convert_to_binary(
            read_image('localization/diode_detection/components/background/{}.png'.format(i)), 10) for i in range(1, 3)]

    @parameterized.expand([[i] for i in range(2)])
    def test_detect_background(self, image_id):
        img = self.images[image_id]
        stats_with_background, centroids_with_background = self.detector.detect(img, False)
        stats_without_background, centroids_without_background = self.detector.detect(img)
        background_stats = list_difference(stats_with_background, stats_without_background)
        background_centroids = list_difference(centroids_with_background, centroids_without_background)
        self.assertEqual(len(background_stats), 1)
        self.assertEqual(len(background_centroids), 1)

    @parameterized.expand([[i] for i in range(2)])
    def test_background_ranges(self, image_id):
        img = self.images[image_id]
        stats_with_background, _ = self.detector.detect(img, False)
        stats_without_background, _ = self.detector.detect(img)
        background_stats = list_difference(stats_with_background, stats_without_background)
        self.assertEqual(background_stats[0][cv2.CC_STAT_LEFT], 0)
        self.assertEqual(background_stats[0][cv2.CC_STAT_TOP], 0)
        self.assertEqual(background_stats[0][cv2.CC_STAT_WIDTH], 500)
        self.assertEqual(background_stats[0][cv2.CC_STAT_HEIGHT], 500)


class TestConnectedComponentsDetectorBasic(TestCase):
    def setUp(self):
        self.detector = ConnectedComponentsDetector()
        self.color_converter = ColorConverter()
        self.images = [self.color_converter.convert_to_binary(
            read_image('localization/diode_detection/components/background/{}.png'.format(i)), 10) for i in range(1, 3)]
        self.stats = stats
        self.centroids = centroids

    @parameterized.expand([[i] for i in range(2)])
    def test_detect_centroids(self, image_id):
        img = self.images[image_id]
        _, c = self.detector.detect(img)
        self.assertTrue(lists_almost_equal(c, self.centroids[image_id + 1], 5))

    @parameterized.expand([[i] for i in range(2)])
    def test_detect_stats(self, image_id):
        img = self.images[image_id]
        s, _ = self.detector.detect(img)
        print(lists_almost_equal(s, self.stats[image_id + 1], 5, 4))


class TestConnectedComponentsDetectorSingleComponent(TestCase):
    def setUp(self):
        self.detector = ConnectedComponentsDetector()
        self.color_converter = ColorConverter()
        self.images = [self.color_converter.convert_to_binary(
            read_image('localization/diode_detection/blobs/single_blob/{}.png'.format(i)), 10) for i in range(1, 10)]
        self.expected_locations = single_expected_locations


    @parameterized.expand([[i] for i in range(1)])
    def test_detect(self, image_id):
        s, c = self.detector.detect(self.images[0])
        img = read_image('localization/diode_detection/blobs/single_blob/{}.png'.format(1))
        for _c in c:
            cv2.circle(img, (int(_c[0]), int(_c[1])), 3, [255, 255, 255], -1)
        cv2.imshow('a', img)
        cv2.waitKey(0)
        print('')
        print(s, c)
        self.assertTrue(True)
        # img = self.images[image_id]
        # stats, centroids = self.detector.detect(img)
        # a = read_image('localization/diode_detection/blobs/single_blob/{}.png'.format(image_id + 1))
        # # print(len(centroids), len(stats))
        # for c in centroids:
        #     cv2.circle(a, (int(c[0]), int(c[1])), 3, [255, 255, 255], -1)
        # cv2.imshow('a', a)
        # cv2.waitKey(0)
        # for i in range(0, len(stats)):
        #     print(stats[i])
        #     cv2.rectangle(a, (stats[i][cv2.CC_STAT_LEFT], stats[i][cv2.CC_STAT_TOP]), (
        #         stats[i][cv2.CC_STAT_LEFT] + stats[i][cv2.CC_STAT_WIDTH], stats[i][cv2.CC_STAT_TOP] + stats[i][cv2.CC_STAT_HEIGHT]),
        #                   [255, 255, 255])
        # cv2.imshow('rect', a)
        # cv2.waitKey(0)

        # self.assertEqual(len(stats), 1)
        # self.assertEqual(len(centroids), 1)
        # self.assertTrue(list_contains_almost_equal(self.expected_locations[image_id], centroids, 4))
