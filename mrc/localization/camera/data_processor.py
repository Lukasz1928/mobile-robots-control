from mrc.localization.camera.utils.diode_detector import DiodeDetector


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

    def __call__(self, image, encoding='bgr', fast=False):
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
        # TODO
        """
        keypoints = self.diode_detector.detect(image, encoding, fast)
        colors = self.diode_color_namer()#part of image with keypoint)
        locations = self.location_calculator.calculate(image, keypoints)
        return locations
