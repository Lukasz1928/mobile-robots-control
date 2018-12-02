from mrc.utils.maths import gauss_distribution


class GaussianHSVPredicate:
    """
    Class representing predicate based on gaussian distribution.

    Intended for internal usage.
    """

    def __call__(self, hue, range_):
        """
        Parameters
        ----------
        hue : `int`
            Value of hue (from HSV color model), range in [0, 360).
        range_ : (`int`, `int`)
            Range of one color to fit hue to.

        Returns
        -------
        `double`
            Probability of hue being of color in given range, value from [0.0, 1.0].
        """
        a, b = range_[0], range_[-1]
        return GaussianHSVPredicate._gaussian_normalized(hue, (a + b) / 2, (a - b) / 8)

    @staticmethod
    def _gaussian_normalized(x, mu, sigma):
        k = 1 / gauss_distribution(mu, mu, sigma)
        return k * gauss_distribution(x, mu, sigma)
