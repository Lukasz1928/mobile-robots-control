from mrc.localization.color.kmeans.analyser import Analyser
from mrc.localization.color.kmeans.defaults import DefaultColorValues
from mrc.localization.color.kmeans.extractor import Extractor


class KMeansStrategy:
    def __init__(self, color_values=DefaultColorValues, fitting_strategy='gaussian'):
        self.analyser = Analyser(predicate_strategy=fitting_strategy, color_values=color_values)
        self.extractor = Extractor(self.analyser)

    def __call__(self, image, blobs):
        return self.extractor.extract(image, blobs)
