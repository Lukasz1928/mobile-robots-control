from abc import ABC, abstractmethod


class AbstractLocationCalculator(ABC):

    @abstractmethod
    def calculate_location(self, point):
        pass
