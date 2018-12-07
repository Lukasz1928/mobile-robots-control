import math

from mrc.utils.maths import gauss_distribution


class PositionPredictor:
    """
    Class responsible for calculation probability of robot being in given angle

    Intended for internal usage.
    """
    def __init__(self, sigma, mu, coef):
        """
        Parameters
        ----------
        sigma : float
            Standard deviation
        mu : float
            Expected value / mean
        coef : float
            Range expansion coefficient
        """
        self.mu = mu
        self.sigma = sigma
        self.coef = coef

    def __call__(self, angle):
        """
        Calculate probability of robot being in given position

        Parameters
        ----------
        angle : float
            Angle at which we see other robot.

        Returns
        -------
        float
            Probability in given rotation_angle
        """
        return gauss_distribution(angle, self.mu, self.sigma)

    def rotate(self, rotation_angle):
        """
        Shift function accordingly to input angle and calculate probability

        Parameters
        ----------
        rotation_angle : float
            Angle to shift function by.

        Returns
        -------
        float
            Probability after rotation.
        """
        self.mu = (self.mu + rotation_angle) % 2 * math.pi
        self.sigma = self.coef * self.sigma
        return gauss_distribution(rotation_angle, self.mu, self.sigma)
