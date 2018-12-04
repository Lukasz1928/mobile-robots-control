from picamera import PiCamera
from picamera.array import PiRGBArray
import math
import numpy as np


class CameraReader:
    def __init__(self, resolution=(640, 480)):
        self.camera = PiCamera()
        self.camera_resolution = (math.ceil(resolution[1] / 16) * 16, math.ceil(resolution[0] / 32) * 32, 3)
        self.camera.resolution = resolution
        self.camera.brightness = 30

    def __call__(self):
        frame = np.empty(self.camera_resolution, dtype=np.uint8)
        self.camera.capture(frame, 'bgr')
        return frame
