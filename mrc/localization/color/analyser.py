from numpy import ndarray
from sklearn.cluster import KMeans

from mrc.localization.color.utils import hsv_pixel_from_centroid
from mrc.localization.color.values import ColorValue, ColorMap


class Analyser:
    def __init__(self):
        self._clusters = 1
        self._estimation_predicate = lambda hsv_value, color_value: \
            1 if hsv_value in ColorMap.color_map[color_value] else 0
        # TODO: Change predicate to fuzzy the hue on hsv circle

    def analyse_chunk(self, image_chunk: ndarray) -> dict:
        pixel_list = image_chunk.reshape(image_chunk.shape[0] * image_chunk.shape[1], 3)
        cluster = KMeans(n_clusters=self._clusters)
        cluster.fit(pixel_list)
        return self._color_analysis(hsv_pixel_from_centroid(cluster.cluster_centers_))

    def _color_analysis(self, hsv_pixel) -> dict:
        (hue, _, _) = hsv_pixel
        result = {}
        for color_val in ColorValue:
            result[color_val] = self._estimation_predicate(hue, color_val)
        return result
