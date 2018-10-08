import cv2

import numpy as np


def calculate_centroid_histogram(clusters):
    numeric_labels = np.arange(0, len(np.unique(clusters.labels_)) + 1)
    (hist, _) = np.histogram(clusters.labels_, bins=numeric_labels)
    return hist.astype("float") / hist.sum()


def hsv_pixel_from_centroid(centroid):
    (r, g, b) = centroid[0].astype('uint8')
    rgb_image = cv2.merge((r, g, b))
    print(rgb_image)
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    print(hsv)


def flatten(seq):
    return sum(seq, [])
