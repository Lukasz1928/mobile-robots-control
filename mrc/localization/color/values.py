from enum import Enum


class ColorValue(Enum):
    red = 'red'
    yellow = 'yellow'
    green = 'green'
    blue = 'blue'


class ColorMap(Enum):
    # Color map has to be updated during the research, values may change
    color_map = {
        ColorValue.red: range(0, 20),
        ColorValue.yellow: range(21, 70),
        ColorValue.green: range(71, 135),
        ColorValue.blue: range(0, -1)  # not used
    }
