import colorsys


def rgb2hsv(r, g, b):
    scaled_rgb = [color / 255 for color in (r, g, b)]
    hsv = colorsys.rgb_to_hsv(*scaled_rgb)
    return tuple(int((color * 360)) for color in hsv)


def chop_blobs(image, blob_coordinates):
    result = []
    for ((x, y), r) in blob_coordinates:
        x, y, r = [int(cord) for cord in (x, y, r)]
        result.append(image[y - 2 * r:y + 2 * r, x - 2 * r:x + 2 * r])
    return result
