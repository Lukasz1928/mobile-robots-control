import math

from mrc.utils.maths import gauss_distribution


class AngularProbability:
    def __init__(self, stdev, mean, coef):
        self.mean = mean
        self.stdev = stdev
        self.coef = coef

    def __call__(self, rotation):
        return gauss_distribution(rotation, self.mean, self.stdev)

    def shift(self, rotation):
        mean = (self.mean + rotation) % (2 * math.pi) - math.pi
        if self.mean > math.pi:
            self.mean = mean - 2 * math.pi
        else:
            self.mean = mean
        self.stdev = self.coef * self.stdev
        return gauss_distribution(rotation, self.mean, self.stdev)
