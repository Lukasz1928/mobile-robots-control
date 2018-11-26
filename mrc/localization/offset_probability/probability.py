import math

from mrc.utils.maths import gauss_distribution


class PositionPredictor:
    def __init__(self, sigma, mu, coef):
        self.mu = mu
        self.sigma = sigma
        self.coef = coef

    def __call__(self, rotation_angle):
        return gauss_distribution(rotation_angle, self.mu, self.sigma)

    def rotate(self, rotation_angle):
        self.mu = (self.mu + rotation_angle) % 2 * math.pi
        self.sigma = self.coef * self.sigma
        return gauss_distribution(rotation_angle, self.mu, self.sigma)
