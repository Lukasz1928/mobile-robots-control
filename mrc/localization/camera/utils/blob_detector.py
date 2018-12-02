import cv2
from mrc.shared.exceptions.exceptions import IncorrectShapeException


class BlobDetector:
    def __init__(self, min_area=None, max_area=None):
        self.detector = self._prepare_detector(min_area, max_area)

    def detect(self, image):
        if len(image.shape) > 3 or (len(image.shape) == 3 and image.shape[2] != 1):
            raise IncorrectShapeException("image must have exactly one channel")
        return self.detector.detect(image)

    @staticmethod
    def _prepare_detector(min_area, max_area):
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 255
        params.filterByCircularity = True
        params.minCircularity = 0.1
        params.filterByInertia = False
        params.filterByConvexity = False
        params.minThreshold = int(0.4 * 255)
        params.maxThreshold = int(255)
        params.thresholdStep = 10
        if min_area is not None or max_area is not None:
            params.filterByArea = True
        if min_area is not None:
            params.minArea = min_area
        if max_area is not None:
            params.maxArea = max_area
        detector = cv2.SimpleBlobDetector_create(params)
        return detector
