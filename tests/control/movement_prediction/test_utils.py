from unittest import TestCase

import numpy as np
from parameterized import parameterized

from mrc.utils.vector import translate_coordinate_system, calculate_movement_vector, sum_vectors
from tests.control.movement_prediction.common import old_vectors, translations, new_vectors, current_positions, \
    movement_vectors, sum_of_vectors


class TestUtils(TestCase):
    @parameterized.expand(zip(old_vectors, translations, new_vectors))
    def test_translate(self, old_vector, translation, expected_vector):
        distance, rotation = translation
        r, theta = translate_coordinate_system(v_old=old_vector, distance=distance, rotation=rotation)
        actual_vector = (r, theta)
        np.testing.assert_almost_equal(expected_vector, actual_vector, decimal=1)

    @parameterized.expand(zip(old_vectors, current_positions, movement_vectors, translations))
    def test_calculate(self, prev_pos, curr_pos, expected_v, translation):
        actual_vector = calculate_movement_vector(prev_pos, curr_pos, translation)
        np.testing.assert_almost_equal(expected_v, actual_vector, decimal=1)

    @parameterized.expand(zip(old_vectors, new_vectors, sum_of_vectors))
    def test_sum_vectors(self, v1, v2, expected):
        actual = sum_vectors(v1, v2)
        np.testing.assert_almost_equal(expected, actual, decimal=1)
