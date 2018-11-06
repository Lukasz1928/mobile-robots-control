from mrc.shared.relativeposition import RelativePosition


class Configurator:
    def __init__(self, master_unit, target_position: RelativePosition):
        self.master_unit = master_unit
        self.target_position = target_position
