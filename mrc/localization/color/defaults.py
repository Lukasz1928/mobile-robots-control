from enum import Enum


class DefaultColorValues(Enum):
    """
    Enum mapping color names into their hue (HSV color model) value from range [0, 360).
    """
    red = range(-30, 30)    # (100, 0 , 0) RGB[0-255]
    yellow = range(30, 90)  # (100, 100, 0) RGB[0-255]
    green = range(90, 150)  # (0, 100, 0) RGB[0-255]
    cyan = range(150, 210)  # (0, 100, 100) RGB[0-255]
    blue = range(210, 270)  # (0, 0, 100) RGB[0-255]
    magenta = range(270, 330)  # (100, 0, 100) RGB[0-255]
