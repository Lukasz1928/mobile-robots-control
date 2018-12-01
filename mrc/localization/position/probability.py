import math

from mrc.utils.maths import gauss_distribution


class AngularProbability:
    def __init__(self, stdev, mean, coef):
        self.mean = mean
        self.stdev = stdev
        self.coef = coef

    def __call__(self, rotation):
        d = math.pi - self.mean
        p1 = gauss_distribution(rotation, self.mean, self.stdev)
        p2 = gauss_distribution(rotation, -math.pi - d, self.stdev)
        return max(p1, p2)

    def reset(self):
        self.stdev /= self.coef

    def shift(self, rotation):
        mean = (self.mean + rotation) % (2 * math.pi) - math.pi
        if self.mean > math.pi:
            self.mean = mean - 2 * math.pi
        else:
            self.mean = mean
        self.stdev = self.coef * self.stdev
        return gauss_distribution(rotation, self.mean, self.stdev)
