from abc import ABC, abstractmethod


class AbstractStrategy(ABC):

    @abstractmethod
    def read(self):
        raise NotImplementedError()

    @abstractmethod
    def think(self):
        raise NotImplementedError()

    @abstractmethod
    def act(self):
        raise NotImplementedError()
