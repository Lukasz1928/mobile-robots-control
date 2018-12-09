from abc import ABC, abstractmethod


class AbstractStrategy(ABC):
    """
    Robot behavior class template.

    Notes
    -----
    This class is abstract and needs to be overridden to be instantiated.
    """

    @abstractmethod
    def read(self, **kwargs):
        """
        First method called in main controller loop.
        It should be responsible for reading environment state.

        Parameters
        ----------
        kwargs
            Optional arguments that might be needed in method implementation.
        """
        pass

    @abstractmethod
    def think(self, **kwargs):
        """
        Second method called in main controller loop.
        It should be responsible for processing read state.

        Parameters
        ----------
        kwargs
            Optional arguments that might be needed in method implementation.
        """
        pass

    @abstractmethod
    def act(self, **kwargs):
        """
        Third method called in main controller loop.
        It should be responsible for issuing proper control commands, according to processed state.

        Parameters
        ----------
        kwargs
            Optional arguments that might be needed in method implementation.
        """
        pass
