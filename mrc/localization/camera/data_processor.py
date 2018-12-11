from collections import OrderedDict
from operator import itemgetter

import cv2

from mrc.localization.calculator.location_calculator import LocationCalculator
from mrc.localization.camera.utils.diode_detector import DiodeDetector
from mrc.localization.color.quick_mean.quick_mean import QuickMeanStrategy
from mrc.localization.color.umpire import ColorUmpire


class FisheyeCameraDataProcessor:
    """
    Class responsible for extracting diode localizations from given image
    """

    def __init__(self, robot_ids, color_namer, location_calculator):
        """
        Parameters
        ----------
        robot_ids : list of Any
            List of robot IDs in environment. Type should be the same as used in `configurator`.
        color_namer : ColorRecognitionStrategy
            Object responsible for recognition of color in image
        location_calculator : AbstractLocationCalculator
            Object responsible for calculating relative location of robot based on its location in photo
        """
        self.robot_ids = robot_ids
        self.diode_detector = DiodeDetector()
        self.diode_color_namer = color_namer
        self.location_calculator = location_calculator

    def __call__(self, image, encoding='BGR', fast=False):
        """
        Run calculations on input image.

        Parameters
        ----------
        image : numpy.ndarray
            Image to detect blobs on. It must be in color encoding specified in `encoding`.
        encoding : str, optional
            String describing image color encoding. Default is 'bgr'
        fast : bool, optional
            Deprecated. Default is False.

        Returns
        -------

        """
        points, stats = self.diode_detector.detect(image, 10, encoding)
        print(points[0].pt, stats)
        if points:
            colors = [self.diode_color_namer(image[y:y + h, x: x + w]) for x, y, w, h, _ in stats]
            x, y, w, h, _ = stats[0]
            cv2.imshow('a', image[y:y + h, x: x + w])
            print(x, y)
            cv2.waitKey(0)
            locations = [self.location_calculator.calculate_location(p.pt) for p in points]
            return {col: loc for (col, loc) in zip(colors, locations)}
        return {}


if __name__ == '__main__':
    processor = FisheyeCameraDataProcessor([], QuickMeanStrategy(),
                                           LocationCalculator((640, 480), lambda x: x + 1, 411))
    image = cv2.imread('C:/Users/wojte/Desktop/raw/blue/141.png')
    print(processor(image))
    #
    # res = []
    # for idx, color in enumerate(colors):
    #     res.append((idx, {k: color[k] for k in sorted(color, key=color.get)}))
    #
    # diode_colors = []
    # for _, d in sorted(res, key=lambda x: x[0]):
    #     k1, v1 = d.popitem()
    #     k2, v2 = d.popitem()
    #     umpired_color = self.umpire.umpire(k1, k2, v1, v2, used_colors)
    #     diode_colors.append(umpired_color)
    # print(diode_colors)
