class PolarPosition:
    def __init__(self, radius: float, angle: float):
        self.angle = angle
        self.radius = radius

    @staticmethod
    def are_positions_approximately_same(location_one, location_two, radius_eps=5, angle_eps=5):
        # TODO: analyse if it makes sense
        return abs(location_one[0] - location_two[0]) < radius_eps and abs(
            location_one[1] - location_two[1]) < angle_eps
