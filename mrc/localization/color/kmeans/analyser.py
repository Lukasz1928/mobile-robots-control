from numpy import ndarray
from sklearn.cluster import KMeans

from mrc.localization.color.kmeans.predicates import GaussianHSVPredicate
from mrc.localization.color.kmeans.utils import hsv_pixel_from_centroid


class Predicates:
    """Container for all available predicates.

    Intended for internal usage.

    Attributes
    ----------
    allowed : :obj:`dict` of {:obj:`str` : Predicate}
        Dictionary, mapping string names of predicates into Predicate objects
    """
    allowed = {
        'gaussian': GaussianHSVPredicate()
    }


class Analyser:
    """
    Class responsible for extracting color from given image chunk.

    Intended for internal use.
    """

    def __init__(self, color_values, predicate_strategy='gaussian'):
        """
        Parameters
        ----------
        color_values : :obj:`Enum`
            Enum object mapping names of colors into their hue (HSV color model) range values.
        predicate_strategy : :obj:`str`, optional
            Optional string with correct name of chosen predicate strategy, default = 'gaussian'.
        """
        self._clusters = 1
        self._resolving_predicate = Predicates.allowed[predicate_strategy]
        self._color_values = color_values

    def analyse_chunk(self, image_chunk: ndarray) -> dict:
        """
        Function counting probabilities of all color occurences in given input.

        Parameters
        ----------
        image_chunk : :obj:`ndarray`
            Array representing fragment of RGB image

        Returns
        -------
            :obj:`dict` of {:obj:`str` : :obj:`float`}
                Color names mapped to probabilities of their occurence in given input.
                Value of probability is between [0.0, 1.0].
        """
        pixel_list = image_chunk.reshape(-1, 3)
        cluster = KMeans(n_clusters=self._clusters)
        cluster.fit(pixel_list)
        return self._color_analysis(hsv_pixel_from_centroid(cluster.cluster_centers_))

    def _color_analysis(self, hsv_pixel) -> dict:
        hue, _, _ = hsv_pixel
        return {color_val.name: self._resolving_predicate(hue, (color_val.value[0], color_val.value[-1])) for color_val
                in
                self._color_values}
