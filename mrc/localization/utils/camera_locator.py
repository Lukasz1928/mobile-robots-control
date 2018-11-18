import colorsys
from typing import Tuple

import numpy
import cv2
#from picamera import PiCamera
#from picamera.array import PiRGBArray
import math
import numpy as np


class CameraReader:
    def __init__(self, resolution=(720, 720)):
        self.camera = PiCamera()
        self.camera_resolution = (math.ceil(resolution[1] / 16) * 16, math.ceil(resolution[0] / 32) * 32, 3)
        self.camera.resolution = resolution
        self.camera.brightness = 30

    def __call__(self):
        frame = numpy.empty(self.camera_resolution, dtype=numpy.uint8)
        self.camera.capture(frame, 'bgr')
        return frame


class CircularIterator:
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius
        self.current_location_vector = [0, radius + 1]
        self.x_range = 0

    def __update_x_range(self):
        if self.current_location_vector[1] in [self.radius, -self.radius]:
            self.x_range = 0
        elif self.current_location_vector[1] >= 0:
            self.x_range = int(math.sqrt(
                self.radius ** 2 + 2 * self.centre[1] * (self.centre[1] + self.current_location_vector[1]) -
                self.centre[1] ** 2 - (self.centre[1] + self.current_location_vector[1]) ** 2))
        else:
            self.x_range = int(math.sqrt(
                self.radius ** 2 + 2 * self.centre[1] * (self.centre[1] + self.current_location_vector[1]) -
                self.centre[1] ** 2 - (self.centre[1] + self.current_location_vector[1]) ** 2))

    def __iter__(self):
        return self

    def __current_location(self):
        return self.centre[0] + self.current_location_vector[0], self.centre[1] + self.current_location_vector[1]

    def __next__(self):
        self.current_location_vector[0] += 1
        if self.current_location_vector[0] > self.x_range:
            self.current_location_vector[1] -= 1
            try:
                self.__update_x_range()
            except ValueError:
                raise StopIteration
            self.current_location_vector[0] = -1 * self.x_range - 1
        return self.__current_location()


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
        return numpy.mean([image[pt[0]][pt[1]] for pt in CircularIterator(centre, radius)], axis=0)

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


img = cv2.imread('C:/Users/Lukasz1928/Desktop/inz/a/img.jpg')
loc = FisheyeCameraLocator(None)
colors = loc(img)
for key in colors.keys():
    colors[key] = FisheyeCameraLocator.bgr2hsv(colors[key])
print(colors)

# reader = CameraReader((750, 600))
# processor = FisheyeCameraLocator(None)
# while True:
#     img = reader()
#     cv2.imshow('img', img)
#     p = processor(img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
