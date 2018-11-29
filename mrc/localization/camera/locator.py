import numpy
import cv2
import math
import numpy as np

from mrc.localization.color.utils.circle_points import CirclePoints


class FisheyeCameraLocator:
    def __init__(self, robots):
        self.robots = robots
        self.blob_detector = FisheyeCameraLocator.prepare_blob_detector()

    def __call__(self, image):
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        leds_image = cv2.inRange(grayscale_image, 125, 255)
        kpts = self.blob_detector.detect(leds_image)
        colors = {}
        for kp in kpts:
            keypoint_color = FisheyeCameraLocator.calculate_blob_color(kp, image)
            colors[kp.pt] = keypoint_color
        return colors

    @staticmethod
    def calculate_blob_color(keypoint, image):
        centre = (int(keypoint.pt[1]), int(keypoint.pt[0]))
        radius = int(keypoint.size / 2)
        return numpy.mean([image[pt[0]][pt[1]] for pt in CirclePoints(centre, radius)], axis=0)

    @staticmethod
    def bgr2hsv(bgr):
        arr = np.ndarray([1, 1, 3], dtype=np.uint8)
        arr[0][0] = bgr
        hsv = cv2.cvtColor(arr, cv2.COLOR_BGR2HSV)
        return [hsv[0][0][0] * 2, hsv[0][0][1] / 2.55, hsv[0][0][2] / 2.55]

    # TODO
    @staticmethod
    def calculate_point_weight(point, centre, radius):
        if (point[0] - centre[0]) ** 2 + (point[1] - centre[1]) ** 2 < radius ** 2 / 4:
            return 1

    @staticmethod
    def prepare_blob_detector():
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 255
        params.filterByCircularity = True
        params.minCircularity = 0.4
        params.filterByInertia = False
        params.filterByConvexity = False
        params.filterByArea = True
        params.maxArea = 250
        params.minArea = 0
        detector = cv2.SimpleBlobDetector_create(params)
        return detector
