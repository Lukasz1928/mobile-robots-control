from numpy import ndarray
from sklearn.cluster import KMeans

from mrc.localization.color.kmeans.predicates import GaussianHSVPredicate
from mrc.localization.color.kmeans.utils import hsv_pixel_from_centroid


class Analyser:
    def __init__(self, predicate_strategy, color_values, color_map):
        self._clusters = 1
        self.allowed_predicates = {
            'gaussian': GaussianHSVPredicate()
        }
        self._resolving_predicate = self.allowed_predicates[predicate_strategy]
        self._color_values = color_values
        self._color_map = color_map

    def analyse_chunk(self, image_chunk: ndarray) -> dict:
        pixel_list = image_chunk.reshape(image_chunk.shape[0] * image_chunk.shape[1], 3)
        cluster = KMeans(n_clusters=self._clusters)
        cluster.fit(pixel_list)
        return self._color_analysis(hsv_pixel_from_centroid(cluster.cluster_centers_))

    def _color_analysis(self, hsv_pixel) -> dict:
        (hue, _, _) = hsv_pixel
        return {color_val: self._resolving_predicate(hue, self._color_map[color_val]) for color_val in
                self._color_values}
