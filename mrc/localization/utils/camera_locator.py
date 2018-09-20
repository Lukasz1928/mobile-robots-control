import numpy
import cv2
# from picamera import PiCamera
# from picamera.array import PiRGBArray
import math


class CameraReader:
    def __init__(self, resolution=(720, 720)):
        self.camera = PiCamera()
        self.camera_resolution = (math.ceil(resolution[1] / 16) * 16, math.ceil(resolution[0] / 32) * 32, 3)
        self.camera.resolution = resolution

    def __call__(self):
        frame = numpy.empty(self.camera_resolution, dtype=numpy.uint8)
        self.camera.capture(frame, 'bgr')
        return frame


class CircularIterator:
    def __init__(self, image, centre, radius):
        self.image = image
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
        return self.image[self.__current_location()]


class FisheyeCameraLocator:
    def __init__(self, robots):
        self.robots = robots
        self.blob_detector = FisheyeCameraLocator.prepare_blob_detector()

    def __call__(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        leds_image = cv2.inRange(gray_image, 225, 255)
        kpts = self.blob_detector.detect(leds_image)
        for kp in kpts:
            FisheyeCameraLocator.calculate_blob_color(kp, image)
        image_with_keypoints = cv2.drawKeypoints(image, kpts, numpy.array([]), (0, 255, 0),
                                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        resolution = (750, 600)
        r = (math.ceil(resolution[1] / 16) * 16, math.ceil(resolution[0] / 32) * 32, 3)
        keypoints_image = cv2.drawKeypoints(numpy.empty(r, dtype=numpy.uint8), kpts, numpy.array([]), (0, 255, 0),
                                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('keypoints_image', keypoints_image)
        cv2.waitKey(1)
        return image_with_keypoints

    @staticmethod
    def calculate_blob_color(keypoint, image):
        centre = (int(keypoint.pt[1]), int(keypoint.pt[0]))
        radius = int(keypoint.size / 2)
        return numpy.mean([pixel for pixel in CircularIterator(img, centre, radius)], axis=0)

    @staticmethod
    def prepare_blob_detector():
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 255
        params.filterByCircularity = True
        params.minCircularity = 0.5
        params.filterByInertia = False
        params.filterByConvexity = False
        params.filterByArea = True
        params.maxArea = 250
        params.minArea = 10
        detector = cv2.SimpleBlobDetector_create(params)
        return detector


# reader = CameraReader((750, 600))
# processor = FisheyeCameraLocator(None)
# while True:
#     img = reader()
#     p = processor(img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
