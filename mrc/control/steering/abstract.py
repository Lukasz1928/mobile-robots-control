from abc import ABC, abstractmethod


class AbstractDTPSteeringInterface(ABC):

    @abstractmethod
    def drive_to_point(self, point):
        raise NotImplementedError()

    @abstractmethod
    def update_data(self, **kwargs):
        raise NotImplementedError()
