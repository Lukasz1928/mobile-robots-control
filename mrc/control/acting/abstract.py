from abc import ABC, abstractmethod


class AbstractStrategy(ABC):

    @abstractmethod
    def read(self, **kwargs):
        pass

    @abstractmethod
    def think(self, **kwargs):
        pass

    @abstractmethod
    def act(self, **kwargs):
        pass
