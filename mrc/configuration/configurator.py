from mrc.shared.position import Position


class Configurator:
    def __init__(self, id_to_location):
        if callable(id_to_location):
            self.is_callable = True
        elif isinstance(id_to_location, dict):
            self.is_callable = False
        else:
            raise ValueError("id_to_location should be either callable or dictionary")
        self.id_to_location = id_to_location

    def _extract_location(self, key) -> Position:
        if self.is_callable:
            return self.id_to_location(key)
        else:
            return self.id_to_location.get(key)

    def get_target_position(self, robot_id) -> Position:
        return self._extract_location(robot_id)
