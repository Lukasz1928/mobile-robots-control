import numpy as np


def _polar2cartesian(vector):
    r, theta = vector
    return np.asarray([r * np.cos(theta), r * np.sin(theta)])


def _cartesian2polar(vector):
    x, y = vector
    return np.asarray([np.sqrt(x ** 2 + y ** 2), np.arctan2(y, x)])


def _fit_angle_in_interval(angle):
    while angle <= -np.pi:
        angle += 2 * np.pi
    while angle > np.pi:
        angle -= 2 * np.pi
    return angle


def _normalize_angle(angle):
    normalized = np.pi / 2 - angle
    return _fit_angle_in_interval(normalized)


def _normalize_polars(coords):
    return coords[0], _normalize_angle(coords[1])


def sum_vectors(*vecs):
    """
    Returns sum of input polar coordinates vectors, in format used by library.

    Parameters
    ----------
    *vecs
        Variable length list of (float, float) array-likes, where first field is distance, second is radius.

    Returns
    -------
    float, float
        Vector, where first field is distance, second is radius.
    """
    norm_vecs_c = [_polar2cartesian(_normalize_polars(vector)) for vector in vecs]
    vec_res = np.sum(norm_vecs_c, axis=0)
    return _normalize_polars(_cartesian2polar(vec_res))


def translate_coordinate_system(v_old, distance, rotation):
    """Function recalculating position of old vector in new coordinate system

    Parameters
    ----------
    v_old : array-like
        Vector in old coordinate system. It should have two fields, first one being radius, second being angle.
    distance : float
        Length of vector that coordinate system was moved along.
    rotation : float
        Angle of coordinate system's rotation in radians.


    Returns
    -------
    ndarray
        Input vector in new coordinate system.

    Notes
    -----
        Angle should be measured clockwise and having value of 0 along vertical coordinate system axis.
        Results for all-zero input might result in undefined behavior.
    """
    r_old, theta_old = v_old
    theta_new = _fit_angle_in_interval(_normalize_angle(theta_old) + rotation) if r_old != 0 else 0
    v_new = _polar2cartesian((r_old, theta_new))
    v_new = np.subtract(v_new, [0, distance])
    r, theta = _cartesian2polar(v_new)
    theta = _normalize_angle(theta)
    return np.asarray((r, theta))


def calculate_movement_vector(pos_prev, pos_current, coord_mov):
    """Function calculating vector of movement between two positions in given time

    Parameters
    ----------
    pos_prev : (float, float)
        Previous position. It should have two fields, first one being radius, second being angle.
    pos_current : (float, float)
        Current position. It should have two fields, first one being radius, second being angle.
    coord_mov : (float, float)
        Vector that coordinate system was translated by. It should have two fields, first one being distance,
        second being rotation.

    Returns
    -------
    float, float
        Calculated vector of movement between given positions in new coordinate system. It will have two fields,
        first one being distance, second being rotation.

    Notes
    -----
        Angle should be measured clockwise and having value of 0 along vertical coordinate system axis.
    """
    distance, rotation = coord_mov
    pos_prev_c = _polar2cartesian(_normalize_polars(
        translate_coordinate_system(pos_prev, distance, rotation))) if pos_prev is not None \
        else _polar2cartesian(_normalize_polars(pos_current))
    pos_current_c = _polar2cartesian(_normalize_polars(pos_current))
    vector = _normalize_polars(_cartesian2polar(np.subtract(pos_current_c, pos_prev_c)))
    return vector
