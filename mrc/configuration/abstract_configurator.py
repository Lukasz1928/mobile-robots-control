from abc import ABC, abstractmethod


class AbstractConfigurator(ABC):
    """
    Configuration holder template.
    """

    @abstractmethod
    def set_identity(self, identity):
        """Method responsible for changing robot identity

        Parameters
        ----------
        identity : Any
            New ID of robot. It has to be compatible with locator.
        """
        pass
