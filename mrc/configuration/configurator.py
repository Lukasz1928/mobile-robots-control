

class Configurator:
    def __init__(self, master_unit, target_position, identity, set_external_identity=None):
        self.master_unit = master_unit
        self.target_position = target_position
        self._identity = identity
        self._set_external_identity = set_external_identity
        self._set_external_identity(self._identity)

    def set_identity(self, identity):
        self._identity = identity
        if self._set_external_identity is not None:
            self._set_external_identity(self._identity)



