from abc import ABC

import chainer
import chainer.functions as F
import chainer.links as L


class AbstractModel(ABC):
    def predict(self, blob):
        pass


class DefaultModel:
    def __init__(self, n_units=100, n_out=6, colors=('red', 'blue', 'green', 'cyan', 'magenta', 'yellow')):
        self.n_units = n_units
        self.n_out = n_out
        self.model = self._net_model()
        self.colors = colors

    def _net_model(self):
        layer = chainer.Sequential(L.Linear(self.n_units), F.relu)
        model = layer.repeat(1)
        model.append(L.Linear(self.n_out))
        return L.Classifier(
            self._net_model(), lossfun=F.sigmoid_cross_entropy, accfun=F.binary_accuracy)

    def _normalize_data(self, image):
        return image.reshape(100, -1, 3)

    def predict(self, blob):
        image = self._normalize_data(blob)
        return self.model.predictor(image[None]).data
