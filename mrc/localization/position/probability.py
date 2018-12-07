import math

from mrc.utils.maths import gauss_distribution


class AngularProbability:
    """
    Class responsible for calculation probability of robot being in given angle

    Intended for internal usage.
    """
    def __init__(self, stdev, mean, coef):
        """
        Parameters
        ----------
        stdev : float
            Standard deviation
        mean : float
            Mean value
        coef : float
            Range expansion coefficient
        """
        self.mean = mean
        self.stdev = stdev
        self.coef = coef

    def __call__(self, rotation):
        """
        Calculate probability of robot being in given position

        Parameters
        ----------
        rotation : float
            Angle at which we see other robot.

        Returns
        -------
        float
            Probability in given rotation_angle
        """
        d = math.pi - self.mean
        p1 = gauss_distribution(rotation, self.mean, self.stdev)
        p2 = gauss_distribution(rotation, -math.pi - d, self.stdev)
        return max(p1, p2)

    def reset(self):
        """
        Reset coefficient to original value
        """
        self.stdev /= self.coef

    def shift(self, rotation):
        """
        Shift function accordingly to input angle and calculate probability

        Parameters
        ----------
        rotation : float
            Angle to shift function by.

        Returns
        -------
        float
            Probability after rotation.
        """
        mean = (self.mean + rotation) % (2 * math.pi) - math.pi
        if self.mean > math.pi:
            self.mean = mean - 2 * math.pi
        else:
            self.mean = mean
        self.stdev = self.coef * self.stdev
        return gauss_distribution(rotation, self.mean, self.stdev)
