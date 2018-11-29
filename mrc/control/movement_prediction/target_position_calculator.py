from mrc.control.movement_prediction.utils import calculate_movement_vector, translate_coordinate_system, sum_vectors


class TargetPositionCalculator:
    """Class responsible for calculating target positions, based on measured master_unit positions.
    """

    def __init__(self, configurator):
        """Predictor constructor

        Parameters
        ----------
        configurator : mrc.configuration.Configurator
            Configuration container, obligatory for getting target position relative to master_unit.
        """
        self._previous_position = None
        self._last_calculated = (0, 0)
        self._configurator = configurator

    def calculate_actual_target_position(self, current_position, movement):
        """Method for calculating target position, without predicting master_unit further movement.

        Parameters
        ----------
        current_position : (double, double)
            Position of master_unit discovered in current measure. It should have two fields, first one being radius,
            second being angle.
        movement : (double, double)
            Vector describing robot's self movement from the previous position. It should have two fields,
            first one being radius, second being angle.

        Returns
        -------
        double, double
            Target position, relative from current_position. It has two fields,
            first one being radius, second being angle.

        Notes
        -----
            This method does not take into account movement of master_unit - it calculates target position
            in the current moment.
        """
        prev_position = self._previous_position
        calculated_vector = calculate_movement_vector(prev_position, current_position, movement)
        self._last_calculated = translate_coordinate_system(self._last_calculated, 0, movement[1])
        if calculated_vector[0] == 0:
            calculated_vector = self._last_calculated if self._last_calculated[0] != 0 else movement
        else:
            self._last_calculated = calculated_vector
        relative_target_position = translate_coordinate_system(self._configurator.target_position, 0,
                                                               calculated_vector[1])
        target_position = sum_vectors(relative_target_position, current_position)
        self._previous_position = current_position
        return target_position

    def predict_further_target_position(self, current_position, movement, multiplier):
        """Method for calculating target position, predicting master_unit further movement.

        Parameters
        ----------
        current_position : (double, double)
            Position of master_unit discovered in current measure. It should have two fields, first one being radius,
            second being angle.
        movement : (double, double)
            Vector describing robot's self movement from the previous position. It should have two fields,
            first one being radius, second being angle.
        multiplier : double
            pass

        Returns
        -------
        double, double
            Target position, predicted basing on master_unit previous moves. It has two fields,
            first one being radius, second being angle.

        Notes
        -----
            This method predicts master_unit further movement, based on its previous moves, and uses that to calculate
            target position in the nearest future.
        """
        target_position = self.calculate_actual_target_position(current_position, movement)
        master_movement = calculate_movement_vector(self._previous_position, current_position, movement)
        return sum_vectors(target_position, (master_movement[0] * multiplier, master_movement[1]))
