

class ExternalIdentitySetter:
    """
    Bridge class between function working on diode and function needed in configuration.
    """
    def __init__(self, set_external_identity, identity_to_external_mapping=None):
        """
        Parameters
        ----------
        set_external_identity : Callable
            Function responsible for changing external robot identity.
        identity_to_external_mapping : dict, optional
            Dict mapping id of robot to format used in diode interface.
            If None, id will be passed directly to diode interface.
            Default = None.
        """
        if identity_to_external_mapping is None:
            self.id2ext = {
                'red': [100, 0, 0],
                'green': [0, 100, 0],
                'blue': [0, 0, 100],
                'cyan': [0, 100, 100],
                'magenta': [100, 0, 100],
                'yellow': [100, 100, 0]
            }
        else:
            self.id2ext = identity_to_external_mapping
        self.set_external_identity = set_external_identity

    def set_identity(self, identity):
        """
        Set external identity of robot

        Parameters
        ----------
        identity : Any
            ID of robot. It should be type used in rest of program.
        """
        external_identity = self.id2ext[identity]
        self.set_external_identity(external_identity)
