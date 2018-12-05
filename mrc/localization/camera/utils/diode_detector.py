from collections import defaultdict

import cv2

from mrc.localization.camera.utils.blob_detector import BlobDetector
from mrc.localization.camera.utils.connected_components_detector import ConnectedComponentsDetector
from mrc.localization.color.utils.color_converter import ColorConverter
from mrc.utils.maths import point_in_rectangle


class DiodeDetector:
    def __init__(self, min_area=1, max_area=None):
        self.blob_detector = BlobDetector(min_area, max_area)
        self.connected_components_detector = ConnectedComponentsDetector()
        self.color_converter = ColorConverter()

    def detect(self, image, threshold=10, color_encoding='BGR'):
        grayscale_image = self.color_converter.convert_to_grayscale(image, color_encoding)
        binary_image = self.color_converter.convert_to_binary(grayscale_image, threshold, color_encoding,
                                                              grayscale=True)
        keypoints = self.blob_detector.detect(grayscale_image)
        stats, centroids = self.connected_components_detector.detect(binary_image)
        ctb_mapping, btc_mapping = self._calculate_image_parts_mapping(keypoints, stats)
        points = [max([(keypoints[bid], keypoints[bid].size / 2) for bid in blob_ids], key=lambda x: x[1])[0] for
                  blob_ids in ctb_mapping.values()]
        areas = [stats[btc_mapping[i]] for p in points for i, k in enumerate(keypoints) if k == p]
        return points, areas

    def _calculate_image_parts_mapping(self, keypoints, stats):
        ctb_mapping = defaultdict(list)
        btc_mapping = {}
        for i, kp in enumerate(keypoints):
            for j, s in enumerate(stats):
                if point_in_rectangle(kp.pt, (s[cv2.CC_STAT_LEFT], s[cv2.CC_STAT_TOP]),
                                      (s[cv2.CC_STAT_WIDTH], s[cv2.CC_STAT_HEIGHT])):
                    ctb_mapping[j].append(i)
                    btc_mapping[i] = j
        return ctb_mapping, btc_mapping
