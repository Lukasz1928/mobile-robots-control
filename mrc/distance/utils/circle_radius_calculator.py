import math
import cv2
import numpy as np
from mrc.localization.color.utils.color_converter import ColorConverter


def calculate_radius(photo):
    cc = ColorConverter()
    blur = cv2.GaussianBlur(photo, (5, 5), 0)
    bin_photo = cc.convert_to_binary(blur, 5)
    if [bin_photo[bin_photo.shape[0] // 2][i] for i in range(bin_photo.shape[1])].count(0) > 0.2 * bin_photo.shape[1]:
        bin_photo = np.transpose(bin_photo)
    whites = [(0, [bin_photo[0][i] for i in range(bin_photo.shape[1])].count(255))]
    for j in range(1, bin_photo.shape[0]):
        wh = [bin_photo[j][i] for i in range(bin_photo.shape[1])].count(255)
        if j <= bin_photo.shape[0] / 2 and wh > whites[len(whites) - 1][1]:
            whites.append((j, wh))
        elif j > bin_photo.shape[0] / 2 and wh < whites[len(whites) - 1][1]:
            whites.append((j, wh))
    return np.mean([math.sqrt((wh / 2.0) ** 2 + (j - bin_photo.shape[0] / 2.0) ** 2) for (j, wh) in whites])
