import colorsys
from typing import Tuple


def hsv_pixel_from_centroid(centroid) -> Tuple[int, ...]:
    """
    Parameters
    ----------
    centroid : `ndarray`
        Array of pixels in centroid, each of them in format (`int`, `int`, `int`) representing RGB

    Returns
    -------
    (`double`, `double`, `double`)
        Color in HSV model.
        Values range inbetween [0, 360).

    Note
    ----
    r, g, b input values should be in range [0, 255].
    """
    (r, g, b) = centroid[0].astype('uint8')
    return rgb2hsv(r, g, b)


def rgb2hsv(r, g, b) -> Tuple[int, ...]:
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
