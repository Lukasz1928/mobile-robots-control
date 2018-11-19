from numpy import ndarray
from sklearn.cluster import KMeans

from mrc.localization.color.kmeans.predicates import GaussianHSVPredicate
from mrc.localization.color.kmeans.utils import hsv_pixel_from_centroid


class Predicates:
    allowed = {
        "gaussian": GaussianHSVPredicate()
    }


class Analyser:
    def __init__(self, color_values, predicate_strategy="gaussian"):
        self._clusters = 1
        self._resolving_predicate = Predicates.allowed[predicate_strategy]
        self._color_values = color_values

    def analyse_chunk(self, image_chunk: ndarray) -> dict:
        pixel_list = image_chunk.reshape(-1, 3)
        cluster = KMeans(n_clusters=self._clusters)
        cluster.fit(pixel_list)
        return self._color_analysis(hsv_pixel_from_centroid(cluster.cluster_centers_))

    def _color_analysis(self, hsv_pixel) -> dict:
        hue, _, _ = hsv_pixel
        return {color_val.name: self._resolving_predicate(hue, color_val.value) for color_val in
                self._color_values}
