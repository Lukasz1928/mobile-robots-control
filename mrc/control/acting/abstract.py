from abc import ABC, abstractmethod


class AbstractStrategy(ABC):

    @abstractmethod
    def read(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def think(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def act(self, **kwargs):
        raise NotImplementedError()
