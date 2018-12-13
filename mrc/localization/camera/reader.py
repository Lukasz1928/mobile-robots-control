import math

import numpy as np
from picamera import PiCamera


class CameraReader:
    """
    Class responsible for reading raw input from Raspberry Pi camera.
    """

    def __init__(self, resolution=(640, 480), brightness=30, contrast=100, sharpness=100, saturation=100):
        """
        Parameters
        ----------
        resolution : (int, int), optional
            Resolution of captured frames, default is 640x480. First number should be multiple of 16,
            second number should be multiple of 32.

        Notes
        -----
        Please do note that bigger images may result in higher calculation accuracy as well as longer processing time.
        """
        self.camera = PiCamera()
        self.camera_resolution = (math.ceil(resolution[1] / 16) * 16, math.ceil(resolution[0] / 32) * 32, 3)
        self.camera.resolution = resolution
        self.camera.brightness = brightness
        self.camera.contrast = contrast
        self.camera.sharpness = sharpness
        self.camera.saturation = saturation
        self.camera.exposure_mode = 'night'
    def __call__(self):
        """
        Captures frame from camera.

        Returns
        -------
        numpy.ndarray
            Array representation of captured frame, colors are encoded in BGR model.
        """
        frame = np.empty(self.camera_resolution, dtype=np.uint8)
        self.camera.capture(frame, 'bgr')
        return frame
