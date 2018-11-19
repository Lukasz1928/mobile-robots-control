import math


class GaussianHSVPredicate:
    def __call__(self, hue, range_):
        a, b = range_[0], range_[-1]
        return GaussianHSVPredicate._gaussian(hue, (a + b) / 2, (a - b) / 8)

    @staticmethod
    def _gaussian(x, mu, sigma):
        k = 1 / GaussianHSVPredicate._raw_gauss(mu, mu, sigma)
        return k * GaussianHSVPredicate._raw_gauss(x, mu, sigma)

    @staticmethod
    def _raw_gauss(x, mu, sigma):
        return 1 / (2 * math.sqrt(math.pi) * sigma) * math.exp(-(1 / 2) * ((x - mu) / sigma) ** 2)
