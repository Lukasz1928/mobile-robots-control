from mrc.localization.camera.utils.diode_detector import DiodeDetector


class FisheyeCameraDataProcessor:
    def __init__(self, robots):
        self.robots = robots
        self.diode_detector = DiodeDetector()
        self.location_calculator = None # TODO add it when it's done

    def __call__(self, image, encoding='bgr', fast=False):
        keypoints = self.diode_detector.detect(image, encoding, fast)
        colors = self.location_calculator.calculate(image, keypoints)
        return colors
