import cv2

from mrc.localization.camera.utils.blob_detector import BlobDetector
from mrc.localization.camera.utils.connected_components_detector import ConnectedComponentsDetector
from mrc.localization.color.utils.color_converter import ColorConverter


class DiodeDetector:

    def __init__(self, min_area=1, max_area=None):
        self.blob_detector = BlobDetector(min_area, max_area)
        self.connected_components_detector = ConnectedComponentsDetector()
        self.color_converter = ColorConverter()

    def detect(self, image, threshold=25, color_encoding='BGR'):
        binary_image = self.color_converter.convert_to_binary(image, threshold, color_encoding)
        keypoints = self.blob_detector.detect(binary_image)
        stats, centroids = self.connected_components_detector.detect(binary_image)
        for c in centroids:
            cv2.circle(image, (int(c[0]), int(c[1])), 3, [255, 255, 255], -1)
        for i in range(1, len(stats)):
            cv2.rectangle(image, (stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP]), (
                stats[i, cv2.CC_STAT_LEFT] + stats[i, cv2.CC_STAT_WIDTH],
                stats[i, cv2.CC_STAT_TOP] + stats[i, cv2.CC_STAT_HEIGHT]),
                          [255, 255, 255])
        cv2.imshow('a', image)
        cv2.waitKey(0)
        return None

    def _detect_diodes(self, keypoints, connected_components):
        pass


img = cv2.imread('C:/Users/Lukasz1928/Desktop/chainer-spike/data/close.png')
d = DiodeDetector()
d.detect(img)
