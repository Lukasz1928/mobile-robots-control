from abc import ABC, abstractmethod


class AbstractDTPSteeringInterface(ABC):

    @abstractmethod
    def drive_to_point(self, point):
        pass

    @abstractmethod
    def update_data(self, **kwargs):
        pass
