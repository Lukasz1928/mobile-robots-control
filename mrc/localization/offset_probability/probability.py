import math

from mrc.utils.maths import gauss_distribution


class AngularProbability:
    def __init__(self, stdev, mean, coef):
        self.mean = mean
        self.stdev = stdev
        self.coef = coef

    def __call__(self, shift):
        return gauss_distribution(shift, self.mean, self.stdev)

    def rotate(self, shift):
        mean = (self.mean + shift) % (2 * math.pi) - math.pi
        if self.mean > math.pi:
            self.mean = mean - 2 * math.pi
        else:
            self.mean = mean
        self.stdev = self.coef * self.stdev
        return gauss_distribution(shift, self.mean, self.stdev)
