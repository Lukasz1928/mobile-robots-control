from enum import Enum


class DefaultColorValues(Enum):
    """
    Enum mapping color names into their hue (HSV color model) value from range [0, 360).
    """
    red = range(-30, 30)
    yellow = range(30, 90)  # (100, 100, 0)
    green = range(90, 150)  # (0, 100, 0)
    cyan = range(150, 210)  # (0, 100, 100)
    blue = range(210, 270)  # (0, 0, 100)
    magenta = range(270, 330)  # (100, 0, 100)
