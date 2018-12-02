from mrc.localization.color.kmeans.analyser import Analyser
from mrc.localization.color.kmeans.defaults import DefaultColorValues
from mrc.localization.color.kmeans.extractor import Extractor


class KMeansStrategy:
    """
    Class representing color extraction strategy.

    Intended for internal usage.
    """

    def __init__(self, color_values=DefaultColorValues, fitting_strategy='gaussian'):
        """
        Parameters
        ----------
        color_values : `Enum`, optional
            Enum mapping color names into their hue (HSV color model) value from range [0, 360).
            Default = `mrc.localization.color.kmeans.defaults.DefaultColorValues`
        fitting_strategy : `str`, optional
            Optional string with correct name of chosen predicate strategy.
            Default = 'gaussian'
        """
        self.analyser = Analyser(predicate_strategy=fitting_strategy, color_values=color_values)
        self.extractor = Extractor(self.analyser)

    def __call__(self, image, blobs):
        """
        Method calling extraction of colors on input image with input blob coordinates.

        Parameters
        ----------
        image : `ndarray`
            Numpy array representing BGR image.
        blobs : ((`float`, `float`), `float`)
            ((x, y), r), where (x,y) are coordinates of blob centers and r is their radius.

        Returns
        -------
        `list` of `str`
            List of color names.
        """
        return self.extractor.extract(image, blobs)
