class PolarPosition:
    """
    Container for position in library-friendly type.

    Attributes
    ----------
    radius : float
        Distance from target
    angle : float
        Clockwise angle counted from movement vector
    """

    def __init__(self, radius: float, angle: float):
        self.angle = angle
        self.radius = radius

    def __setitem__(self, key, value):
        {0: self.angle, 1: self.radius}[key] = value

    def __getitem__(self, item):
        return {0: self.angle, 1: self.radius}

    @staticmethod
    def are_positions_approximately_same(location_one, location_two, radius_eps=5, angle_eps=0.2):
        """
        Checks if given two locations are almost same

        Parameters
        ----------
        location_one : (float, float)
            (radius, angle) of first location
        location_two : (float, float)
            (radius, angle) of second location
        radius_eps : float
            Allowed difference between radiuses
        angle_eps : float
            Allowed differences between angles

        Returns
        -------
        bool
            True if difference between locations is below given epsilons.
        """
        return abs(location_one[0] - location_two[0]) < radius_eps and abs(
            location_one[1] - location_two[1]) < angle_eps
