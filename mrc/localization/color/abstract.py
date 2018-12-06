from abc import ABC, abstractmethod


class ColorRecognitionStrategy(ABC):

    @abstractmethod
    def __call__(self, image):
        pass
