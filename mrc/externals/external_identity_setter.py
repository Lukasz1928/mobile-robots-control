

class ExternalIdentitySetter:
    def __init__(self, set_external_identity, identity_to_external_mapping=None):
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
        external_identity = self.id2ext[identity]
        self.set_external_identity(external_identity)
