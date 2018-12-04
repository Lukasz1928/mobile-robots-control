from enum import Enum


class DefaultColorValues(Enum):
    """
    Enum mapping color names into their hue (HSV color model) value from range [0, 360).
    """
    red = range(0, 20)
    yellow = range(21, 70)
    green = range(71, 135)
