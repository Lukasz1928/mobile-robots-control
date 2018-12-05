import math


def gauss_distribution(x, mu, sigma):
    return 1 / (2 * math.sqrt(math.pi) * sigma) * math.exp(-(1 / 2) * ((x - mu) / sigma) ** 2)


def points_2d_sqr_distance(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def points_2d_distance(p1, p2):
    return math.sqrt(points_2d_sqr_distance(p1, p2))


def vector_2d_length(vec):
    return points_2d_sqr_distance(vec, (0, 0))


def point_in_rectangle(point, rect_top_left, rect_sides):
    return rect_top_left[0] < point[0] < rect_top_left[0] + rect_sides[0] and \
           rect_top_left[1] < point[1] < rect_top_left[1] + rect_sides[1]


def rescale_rectangle(top_left, sides, ratio):
    rescaled_top_left = (top_left[0] + sides[0] / 2.0 - sides[0] / math.sqrt(2.0),
                         top_left[1] + sides[1] / 2.0 - sides[1] / math.sqrt(2.0))
    rescaled_sides = (sides[0] * ratio, sides[1] * ratio)
    return rescaled_top_left, rescaled_sides


def normalize_point_in_circle(point, resolution, radius):
    image_centre = (resolution[0] // 2, resolution[1] // 2)
    point_vector = [image_centre[0] - point[0], point[1] - image_centre[1]]
    npv = [point_vector[0] / radius, point_vector[1] / radius]
    return npv