from collections import defaultdict
import cv2
from mrc.localization.camera.utils.blob_detector import BlobDetector
from mrc.localization.camera.utils.connected_components_detector import ConnectedComponentsDetector
from mrc.localization.color.utils.color_converter import ColorConverter
from mrc.utils.maths import point_in_rectangle
import numpy as np


class DiodeDetector:
    """
    Class responsible for detecting diodes locations.

    Intended for internal usage.
    """
    def __init__(self, min_area=1, max_area=None):
        """
        Parameters
        ----------
        min_area : int, optional
            Smallest area of blob to count as diode. Default = 1.
        max_area : int, optional
            Biggest area of blob to count as diode. Default is None.
        """
        self.blob_detector = BlobDetector(min_area, max_area)
        self.connected_components_detector = ConnectedComponentsDetector()
        self.color_converter = ColorConverter()

    def detect(self, image, threshold=10, color_encoding='BGR'):
        """
        Parameters
        ----------
        image : numpy.ndarray
            Image to detect blobs on. It must be in color encoding specified in `color_encoding`.
        threshold : int, optional
            Border of classifying gray-scale value as either white or black in binarization of image.
            Values above threshold will be classified as white, below as black. Default is 10.
        color_encoding : str, optional
            String describing image color encoding. Default is 'BGR'

        Returns
        -------
        list of `cv.Keypoint`, list of list
            First one is list of Keypoints corresponding to found diodes.
            Second one is list of five-element lists, containing info about image areas diodes were found in.

        Notes
        -----
        So far, the only color encodings accepted are 'BGR' and 'RGB'.

        """
        grayscale_image = self.color_converter.convert_to_grayscale(image, color_encoding)
         
        binary_image = self.color_converter.convert_to_binary(grayscale_image, threshold, color_encoding,
                                                              grayscale=True)
        stats, centroids = self.connected_components_detector.detect(binary_image)
        print('s ' + str(stats))
        keypoints = []
        for s in stats:
            kp = self.blob_detector.detect(grayscale_image[s[1]:s[1]+s[3],s[0]:s[0]+s[2]])
            for p in kp:
                p.pt = (p.pt[0] + s[0], p.pt[1] + s[1])
            keypoints.extend(kp)        
        return keypoints, stats

dd = DiodeDetector()
img = cv2.imread('C:/Users/Lukasz1928/Desktop/inz/mobile-robots-control/tests/resources/localization/diode_detection/blobs/single_blob/1.png')
a, b = dd.detect(img)
print(a)
print(b)
