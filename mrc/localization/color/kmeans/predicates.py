from mrc.utils.maths import gauss_distribution


class GaussianHSVPredicate:
    def __call__(self, hue, range_):
        a, b = range_[0], range_[-1]
        return GaussianHSVPredicate._gaussian_normalized(hue, (a + b) / 2, (a - b) / 8)

    @staticmethod
    def _gaussian_normalized(x, mu, sigma):
        k = 1 / gauss_distribution(mu, mu, sigma)
        return k * gauss_distribution(x, mu, sigma)
