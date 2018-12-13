from mrc.configuration.abstract_configurator import AbstractConfigurator


class Configurator(AbstractConfigurator):
    """
    Container for data about robot's position in formation.
    """
    def __init__(self, master_unit, target_position, identity, set_external_identity=None):
        """
        Parameters
        ----------
        master_unit : Any
            ID of master unit. It has to be compatible with locator.
        target_position : (double, double)
            Target position relative to master unit. First field is distance, second is angle.
        identity : Any
            ID of robot. It has to be compatible with locator.
        set_external_identity : :obj:`Any -> Any`, optional
            Optional function responsible for changing robot identity outside `Configurator`.
            It has to accept `identity` as its only argument.

        Notes
        -----
        Master unit is the robot that the one the program is running on is supposed to follow.

        """
        self.master_unit = master_unit
        self.target_position = target_position
        self._identity = identity
        self._set_external_identity = set_external_identity
        self.set_identity(self._identity)

    def set_identity(self, identity):
        """Method responsible for changing robot identity

        Parameters
        ----------
        identity : Any
            New ID of robot. It has to be compatible with locator.
        """
        self._identity = identity
        if self._set_external_identity is not None:
            self._set_external_identity(self._identity)



