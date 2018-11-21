from unittest import TestCase

import numpy as np
from parameterized import parameterized

from mrc.control.movement_prediction.utils import translate


class TestUtils(TestCase):
    old_vectors = [
        [0, 0],
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
        [0, 0],
        [2, np.deg2rad(180)],
        [2, np.deg2rad(-90)],
        [2, np.deg2rad(-90)],
        [3 * np.sqrt(2), np.deg2rad(-135)],
    ]
    new_vectors_r = [[np.round(r, 5), np.round(theta, 5)] for r, theta in new_vectors]

    @parameterized.expand(zip(old_vectors, translations, new_vectors_r))
    def test_translate(self, old_vector, translation, expected_vector):
        distance, rotation = translation
        r, theta = translate(v_old=old_vector, distance=distance, rotation=rotation)
        actual_vector_r = list((np.round(r, 5), np.round(theta, 5)))
        self.assertListEqual(expected_vector, actual_vector_r)
