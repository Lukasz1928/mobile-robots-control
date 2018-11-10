from enum import Enum


class DefaultColorValue(Enum):
    red = 'red'
    yellow = 'yellow'
    green = 'green'


class DefaultColorMap:
    color_map = {
        DefaultColorValue.red: range(0, 20),
        DefaultColorValue.yellow: range(21, 70),
        DefaultColorValue.green: range(71, 135),
    }
