import math


def gauss_distribution(x, mu, sigma):
    return 1 / (2 * math.sqrt(math.pi) * sigma) * math.exp(-(1 / 2) * ((x - mu) / sigma) ** 2)
