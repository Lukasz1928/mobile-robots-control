from mrc.localization.camera.utils.diode_detector import DiodeDetector


class FisheyeCameraDataProcessor:
    """
    Class responsible for extracting diode localizations from given image
    """
    def __init__(self, robot_ids):
        """
        Parameters
        ----------
        robot_ids : list of Any
            List of robot IDs in environment. Type should be the same as used in `configurator`.
        """
        self.robot_ids = robot_ids # TODO: it will be used when everything is ready to use
        self.diode_detector = DiodeDetector()
        self.location_calculator = None  # TODO: add it when it's done

    def __call__(self, image, encoding='bgr', fast=False):
        """
        Run calculations on imput image.

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
        colors = self.location_calculator.calculate(image, keypoints)
        return colors
