from unittest import TestCase
from unittest.mock import Mock

import numpy as np
from parameterized import parameterized

from mrc.control.movement_prediction.target_position_calculator import TargetPositionCalculator
from mrc.control.movement_prediction.utils import sum_vectors, translate_coordinate_system, calculate_movement_vector
from tests.control.movement_prediction.common import old_vectors, current_positions, movement_vectors, translations, \
    new_vectors


class TestTargetPositionCalculator(TestCase):
    def setUp(self):
        self.configuration = Mock()
        self.target_position_calculator = TargetPositionCalculator(self.configuration)

    @parameterized.expand(zip(old_vectors, current_positions, translations, movement_vectors, new_vectors))
    def test_calculate_actual_target_position(self, old_v, curr_v, transl_v, mov_v, tar_v):
        self.configuration.target_position = tar_v
        modified_target_position = translate_coordinate_system(self.configuration.target_position, 0, mov_v[1])
        self.target_position_calculator._previous_position = old_v
        actual_v = self.target_position_calculator.calculate_actual_target_position(curr_v, transl_v)
        np.testing.assert_almost_equal(sum_vectors(modified_target_position, curr_v), actual_v, decimal=1)

    @parameterized.expand(
        zip(old_vectors, current_positions, translations, movement_vectors, new_vectors, np.linspace(0.2, 1, 5)))
    def test_predict_further_target_position(self, old_v, curr_v, transl_v, mov_v, tar_v, multiplier):
        self.configuration.target_position = tar_v
        modified_target_position = translate_coordinate_system(self.configuration.target_position, 0, mov_v[1])
        self.target_position_calculator._previous_position = old_v
        actual_v = self.target_position_calculator.predict_further_target_position(curr_v, transl_v, multiplier)
        master_movement = calculate_movement_vector(old_v, curr_v, transl_v)
        np.testing.assert_almost_equal(
            sum_vectors(modified_target_position, curr_v, (master_movement[0] * multiplier, master_movement[1])),
            actual_v, decimal=1)
