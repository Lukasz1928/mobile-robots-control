from mrc.utils.vector import calculate_movement_vector, translate_coordinate_system, sum_vectors


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

    def calculate_actual_target_position(self, current_position, movement, epsilon=1e-3):
        """Method for calculating target position, without predicting master_unit further movement.

        Parameters
        ----------
        current_position : (float, float)
            Position of master_unit discovered in current measure. It should have two fields, first one being radius,
            second being angle.
        movement : (float, float)
            Vector describing robot's self movement from the previous position. It should have two fields,
            first one being radius, second being angle.
        epsilon : :obj:`float`, optional
            Calculation precision, values below epsilon can be treated as 0. Default value = 1e-3.


        Returns
        -------
        float, float
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
            calculated_vector = self._last_calculated if self._last_calculated[0] < epsilon else (0, 0)
        else:
            self._last_calculated = calculated_vector
        relative_target_position = translate_coordinate_system(self._configurator.target_position, 0,
                                                               calculated_vector[1])
        target_position = sum_vectors(relative_target_position, current_position)
        self._previous_position = current_position
        return target_position

    def predict_further_target_position(self, current_position, movement, multiplier=1, epsilon=1e-3):
        """Method for calculating target position, predicting master_unit further movement.

        It adds master_unit movement vector (length multiplied by multiplier) to calculated actual target position.

        Parameters
        ----------
        current_position : (float, float)
            Position of master_unit discovered in current measure. It should have two fields, first one being radius,
            second being angle.
        movement : (float, float)
            Vector describing robot's self movement from the previous position. It should have two fields,
            first one being radius, second being angle.
        multiplier : :obj:`float`, optional
            Value describing movement vector length modifier, default = 1.
        epsilon : :obj:`float`, optional
            Calculation precision, values below epsilon can be treated as 0. Default value = 1e-3.

        Returns
        -------
        float, float
            Target position, predicted basing on master_unit previous moves. It has two fields,
            first one being radius, second being angle.

        Notes
        -----
            This method predicts master_unit further movement, based on its previous moves, and uses that to calculate
            target position in the nearest future.

            Multiplier parameter should be used with value proportional to differences in time between last
            and current measure - if previously master_unit movement was measured in N time, and now it's measured
            in e.g. 1,2N time, multiplier should be 1,2. It should prevent our unit from going out of sync
            with master_unit due to difference between timedeltas in previous and current measures.
        """
        target_position = self.calculate_actual_target_position(current_position, movement, epsilon)
        return sum_vectors(target_position, (self._last_calculated[0] * multiplier, self._last_calculated[1]))
