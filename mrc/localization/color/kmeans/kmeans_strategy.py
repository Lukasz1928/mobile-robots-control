from mrc.localization.color.kmeans.analyser import Analyser
from mrc.localization.color.kmeans.defaults import DefaultColorValue, DefaultColorMap
from mrc.localization.color.kmeans.extractor import Extractor


class KMeansStrategy:
    def __init__(self, color_values=DefaultColorValue, color_map=DefaultColorMap.color_map,
                 fitting_strategy='gaussian'):
        self.allowed_strategies = ['gaussian']
        self.analyser = Analyser(fitting_strategy, color_values, color_map)
        self.extractor = Extractor(self.analyser)

    def __call__(self, image, blobs):
        return self.extractor.extract(image, blobs)
