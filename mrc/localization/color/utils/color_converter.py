import colorsys
import cv2
from mrc.shared.exceptions.exceptions import ColorEncodingNotSupportedException


class ColorConverter:
    encoding_modifiers = {'BGR': [cv2.COLOR_BGR2GRAY], 'RGB': [cv2.COLOR_RGB2GRAY]}

    def convert_to_grayscale(self, image, color_encoding='BGR'):
        conversion_types = self._get_grayscale_color_conversion_code(color_encoding)
        for conversion in conversion_types:
            image = cv2.cvtColor(image, conversion)
        return image

    def convert_to_binary(self, image, threshold, color_encoding='BGR', grayscale=False):
        gray = self.convert_to_grayscale(image, color_encoding) if not grayscale else image
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return binary

    def _get_grayscale_color_conversion_code(self, color_encoding):
        if color_encoding not in self.encoding_modifiers:
            raise ColorEncodingNotSupportedException(
                "{} color encoding is not supported. Supported encodings are {}".format(color_encoding,
                                                                                        self.encoding_modifiers.keys()))
        return self.encoding_modifiers[color_encoding]


def rgb2hsv(r, g, b):
    """
    Parameters
    ----------
    r : `int`
        Value of intensity of red in RGB model
    g : `int`
        Value of intensity of green in RGB model
    b : `int`
        Value of intensity of blue in RGB model

    Returns
    -------
    (`double`, `double`, `double`)
        Color in HSV model.
        Values range inbetween [0, 360).

    Note
    ----
    r, g, b input values should be in range [0, 255].
    """
    scaled_rgb = [color / 255 for color in (r, g, b)]
    hsv = colorsys.rgb_to_hsv(*scaled_rgb)
    return tuple(int((color * 360)) for color in hsv)
