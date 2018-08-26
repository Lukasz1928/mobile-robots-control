import numpy
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray


class CameraReader:
    def __init__(self, resolution=(720, 720)):
        self.camera = PiCamera()
        self.camera_resolution = (math.ceil(resolution[1] / 16) * 16, math.ceil(resolution[0] / 32) * 32, 3)
        print('cr: ' + str(self.camera_resolution))
        self.camera.resolution = resolution

    def __call__(self):
        frame = numpy.empty(self.camera_resolution, dtype=numpy.uint8)
        self.camera.capture(frame, 'bgr')
        return frame


class FisheyeCameraLocator:
    def __init__(self, robots):
        self.robots = robots

    def __call__(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (7, 7), 0) # TODO: check different kernel sizes



