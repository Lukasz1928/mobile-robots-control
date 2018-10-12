import colorsys
from typing import Tuple


def hsv_pixel_from_centroid(centroid) -> Tuple[int, ...]:
    (r, g, b) = centroid[0].astype('uint8')
    return rgb2hsv(r, g, b)


def rgb2hsv(r, g, b) -> Tuple[int, ...]:
    scaled_rgb = [color / 255 for color in (r, g, b)]
    hsv = colorsys.rgb_to_hsv(*scaled_rgb)
    return tuple([int((color * 360)) for color in hsv])
