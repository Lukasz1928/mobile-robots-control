import warnings
import cv2
from mrc.localization.color.utils.color_conversion import hsv2grayscale


class ColorEncodingNotSupportedException(Exception):
    pass


class DiodeDetector:
    encoding_modifiers = {'BGR': [cv2.COLOR_BGR2GRAY], 'RGB': [cv2.COLOR_RGB2GRAY],
                          'HSV': [cv2.COLOR_HSV2BGR, cv2.COLOR_BGR2GRAY]}
    special_encoding_modifiers = {'HSV': [hsv2grayscale]}

    def __init__(self, min_area=1, max_area=250):
        self.detector = self.prepare_blob_detector(min_area, max_area)

    # if special -> search in special_encodings_modifiers
    #   if found -> use found modifier
    #   if not found -> search in encoding_modifier
    # if not special -> use conversion from encoding_modifier
    def detect(self, image, color_encoding='BGR', special=False):
        if special and color_encoding in self.special_encoding_modifiers:
            for conversion in self.special_encoding_modifiers[color_encoding]:
                image = conversion(image)
        else:
            conversion_types = self._get_color_convertion_code(color_encoding, special)
            for conversion in conversion_types:
                image = cv2.cvtColor(image, conversion)
        keypoints = self.detector.detect(image)
        return keypoints

    def _get_color_convertion_code(self, color_encoding, fast):
        if color_encoding not in self.encoding_modifiers:
            raise ColorEncodingNotSupportedException(
                "{} color encoding is not supported. Supported encodings are {}".format(color_encoding,
                                                                                        self.encoding_modifiers.keys()))
        return self.encoding_modifiers[color_encoding]

    @staticmethod
    def prepare_blob_detector(min_area, max_area):
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 255
        params.filterByCircularity = True
        params.minCircularity = 0.4
        params.filterByInertia = False
        params.filterByConvexity = False
        params.filterByArea = True
        params.maxArea = max_area
        params.minArea = min_area
        detector = cv2.SimpleBlobDetector_create(params)
        return detector
