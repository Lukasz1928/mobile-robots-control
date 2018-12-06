import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np

from mrc.localization.color.abstract import ColorRecognitionStrategy


class DefaultModel:
    def __init__(self, n_units=100, n_out=6):
        self.n_units = n_units
        self.n_out = n_out

    def __call__(self, *args, **kwargs):
        L.Classifier(
            self._net_model(), lossfun=F.sigmoid_cross_entropy, accfun=F.binary_accuracy)

    def _net_model(self):
        layer = chainer.Sequential(L.Linear(self.n_units), F.relu)
        model = layer.repeat(1)
        model.append(L.Linear(self.n_out))
        return model


class NeuralNetworkRecognitionStrategy(ColorRecognitionStrategy):
    def __init__(self, model_path="models/diodes_set933.model",
                 model_class=DefaultModel(), detectable_colors=('red', 'blue', 'green', 'cyan', 'magenta', 'yellow')):
        self.model = model_class()
        self.colors = detectable_colors
        chainer.serializers.load_npz(model_path, self.model)

    def __call__(self, blob):
        blob = np.array(blob[:], dtype=np.float32)
        d: np.ndarray = self.model.predictor(blob[None]).data
        k = int(np.argmax(d))
        return self.colors[k]
