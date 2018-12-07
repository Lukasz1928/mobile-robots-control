import math


class CirclePoints:
    """
    Class responsible for helping to iterate through circle points.

    Intended for internal usage.
    """
    def __init__(self, centre, radius):
        """
        Parameters
        ----------
        centre : (int, int)
            x, y coordinates of circle center.
        radius : int
            radius of circle.
        """
        self.centre = centre
        self.radius = radius
        self.current_location_vector = [0, radius + 1]
        self.x_range = 0

    def _update_x_range(self):
        if self.current_location_vector[1] in [self.radius, -self.radius]:
            self.x_range = 0
        else:
            self.x_range = int(math.sqrt(
                self.radius ** 2 + 2 * self.centre[1] * (self.centre[1] + self.current_location_vector[1]) -
                self.centre[1] ** 2 - (self.centre[1] + self.current_location_vector[1]) ** 2))

    def __iter__(self):
        return self

    def _current_location(self):
        return self.centre[0] + self.current_location_vector[0], self.centre[1] + self.current_location_vector[1]

    def __next__(self):
        self.current_location_vector[0] += 1
        if self.current_location_vector[0] > self.x_range:
            self.current_location_vector[1] -= 1
            try:
                self._update_x_range()
            except ValueError:
                raise StopIteration
            self.current_location_vector[0] = -1 * self.x_range - 1
        return self._current_location()
