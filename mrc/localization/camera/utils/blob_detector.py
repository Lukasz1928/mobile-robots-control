import cv2
import numpy as np
from mrc.shared.exceptions.exceptions import IncorrectShapeException


class BlobDetector:
    """
    Class responsible for detecting blobs

    Intended for internal usage.
    """
    def __init__(self, min_area=None, max_area=None):
        """
        Parameters
        ----------
        min_area : int, optional
            Smallest area of blob to detect. Default is None.
        max_area : int, optional
            Biggest area of blob to detect. Default is None.
        """
        self.detector = self._prepare_detector(min_area, max_area)

    def detect(self, image):
        """
        Find positions of blobs from given image.

        Parameters
        ----------
        image : `numpy.ndarray`
            Image to detect blobs on. It must be grayscale, one-channel.

        Returns
        -------
        list of `cv.Keypoint`
            List of all Keypoints corresponding to found blobs.

        Raises
        ------
        `IncorrectShapeException`
            Exception raised in case of image not being one-channel grayscale.

        """
        if len(image.shape) > 3 or (len(image.shape) == 3 and image.shape[2] != 1):
            raise IncorrectShapeException("image must have exactly one channel")
        return self.detector.detect(image)

    @staticmethod
    def _prepare_detector(min_area, max_area):
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 255
        params.filterByCircularity = True
        params.minCircularity = 0.5
        params.filterByInertia = False
        params.filterByConvexity = False
        params.minThreshold = int(1)
        params.maxThreshold = int(255)
        params.thresholdStep = 25
        if min_area is not None or max_area is not None:
            params.filterByArea = True
        if min_area is not None:
            params.minArea = min_area
        if max_area is not None:
            params.maxArea = max_area
        detector = cv2.SimpleBlobDetector_create(params)
        return detector
