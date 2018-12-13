import math


def gauss_distribution(x, mu, sigma):
    """
    Calculate value of gauss (normal) distribution

    Parameters
    ----------
    x : float
        Input argument
    mu :
        Mean of distribution
    sigma :
        Standard deviation

    Returns
    -------
    float
        Probability, values from range [0-1]
    """
    return 1 / (2 * math.sqrt(math.pi) * sigma) * math.exp(-(1 / 2) * ((x - mu) / sigma) ** 2)


def points_2d_sqr_distance(p1, p2):
    """
    Calculate square of distance between two points in two-dimensional space

    Parameters
    ----------
    p1 : (float, float)
        First point
    p2 : (float, float)
        Second point

    Returns
    -------
    float
        Square of distance between two points
    """
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def points_2d_distance(p1, p2):
    """
    Calculate distance between two points in two-dimensional space

    Parameters
    ----------
    p1 : (float, float)
        First point
    p2 : (float, float)
        Second point

    Returns
    -------
    float
        Distance between two points
    """
    return math.sqrt(points_2d_sqr_distance(p1, p2))


def vector_2d_length(vec):
    """
    Calculate vector length in two-dimensional space

    Parameters
    ----------
    vec : (float, float)
        Vector

    Returns
    -------
    float
        Length of vector
    """
    return points_2d_distance(vec, (0, 0))


def point_in_rectangle(point, rect_top_left, rect_sides):
    """
    Checks if point is in rectangle

    Parameters
    ----------
    point : (float, float)
        (x,y) coordinates of point
    rect_top_left : (float, float)
        (x,y) coordinates of rectangle top left corner
    rect_sides : (float, float)
        (x,y) lengths of rectangle sides

    Returns
    -------
    bool
        True if point is in rectangle, otherwise False.
    """
    return rect_top_left[0] < point[0] < rect_top_left[0] + rect_sides[0] and \
           rect_top_left[1] < point[1] < rect_top_left[1] + rect_sides[1]


def rescale_rectangle(top_left, sides, ratio):
    """
    Rescale rectangle, leaving its center point unchanged

    Parameters
    ----------
    top_left : (float, float)
        (x,y) coordinates of rectangle top left corner
    sides : (float, float)
        (x,y) lengths of rectangle sides
    ratio : float
        Rescale value

    Returns
    -------
    (float, float), (float, float)
        Rescaled top left corner coordinates, rescaled lengths of sides
    """
    rescaled_top_left = (top_left[0] + sides[0] / 2.0 - sides[0] / 2.0 * ratio,
                         top_left[1] + sides[1] / 2.0 - sides[1] / 2.0 * ratio)
    rescaled_sides = (sides[0] * ratio, sides[1] * ratio)
    return rescaled_top_left, rescaled_sides


def normalize_point_in_circle(point, resolution, radius):
    """
    Calculates normalized distance between point and center of picture in middle of picture

    Parameters
    ----------
    point : (float, float)
        (x,y) coordinates of point
    resolution : (int, int)
        (width, height) resolution of picture
    radius : float
        Length of circle radius

    Returns
    -------
    float
        Normalized length in range [0, 1]
    """
    image_centre = (resolution[0] // 2, resolution[1] // 2)
    point_vector = [image_centre[1] - point[1], point[0] - image_centre[0]]
    npv = [point_vector[0] / radius, point_vector[1] / radius]
    return npv
