from abc import ABC, abstractmethod


class AbstractDTPSteeringInterface(ABC):
    """
    Robot steering interface template.

    Notes
    -----
    This class is abstract and needs to be overridden to be instantiated.
    """

    @abstractmethod
    def drive_to_point(self, point):
        """
        Move unit to specified point

        Parameters
        ----------
        point : (float, float)
            Target position.
            First field is distance, second field is angle.
        """
        pass

    @abstractmethod
    def update_data(self, **kwargs):
        """
        Update information about environment in the steering interface.
        Implemented in case it should have information about environment.

        Parameters
        ----------
        kwargs
            Named arguments for usage in method implementation
        """
        pass
