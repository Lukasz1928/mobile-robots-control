from abc import ABC, abstractmethod


class AbstractConfigurator(ABC):

    @abstractmethod
    def set_identity(self, identity):
        pass
