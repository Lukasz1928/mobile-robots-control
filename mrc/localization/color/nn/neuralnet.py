

import chainer
import numpy as np

from mrc.localization.color.abstract import ColorRecognitionStrategy
from mrc.localization.color.nn.models import DefaultModel


class NeuralNetworkRecognitionStrategy(ColorRecognitionStrategy):
    def __init__(self, model_path="models/diodes_set933.model",
                 model=DefaultModel()):
        self.model = model
        self.colors = model.colors
        chainer.serializers.load_npz(model_path, self.model)

    def __call__(self, blob):
        blob = np.array(blob[:], dtype=np.float32)
        d: np.ndarray = self.model.predict(blob)
        k = int(np.argmax(d))
        return self.colors[k]
