import cv2
import numpy as np


class KalmanPredictor:
    def __init__(self):
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.kf.measurementNoiseCov = np.array([[1, 0], [0, 1]], np.float32)
        self.kf.processNoiseCov = np.array(
            [[10e-5, 0, 10e-5, 0], [0, 10e-5, 0, 10e-5], [0, 0, 10e-5, 0], [0, 0, 0, 10e-5]],
            np.float32)

    def update(self, r, phi):
        measurement = np.array([[np.float32(r)], [np.float32(phi)]])
        self.kf.correct(measurement)

    def predict(self):
        return self.kf.predict()