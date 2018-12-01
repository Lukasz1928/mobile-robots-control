from unittest import TestCase

import numpy as np
from parameterized import parameterized

from mrc.control.movement_prediction.utils import translate_coordinate_system, calculate_movement_vector


class TestUtils(TestCase):
    old_vectors = [
        [1, 0],
        [0, 0],
        [2 * np.sqrt(2), np.deg2rad(45)],
        [2 * np.sqrt(2), np.deg2rad(-90)],
        [3, np.deg2rad(135)],
    ]
    translations = [
        [0, 0],
        [2, 0],
        [2, np.deg2rad(90)],
        [2, np.deg2rad(-45)],
        [3, np.deg2rad(-135)],
    ]
    new_vectors = [
        [1, 0],
        [2, np.deg2rad(180)],
        [2, np.deg2rad(-90)],
        [2, np.deg2rad(-90)],
        [3 * np.sqrt(2), np.deg2rad(-135)],
    ]
    current_positions = [
        [4, 0],
        [2, np.deg2rad(90)],
        [1, np.deg2rad(-90)],
        [2 * np.sqrt(2), np.deg2rad(-45)],
        [np.sqrt(2), np.deg2rad(45)],
    ]
    movement_vectors = [
        [3, 0],
        [2 * np.sqrt(2), np.deg2rad(45)],
        [1, np.deg2rad(90)],
        [2, 0],
        [4 * np.sqrt(2), np.deg2rad(45)],
    ]

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