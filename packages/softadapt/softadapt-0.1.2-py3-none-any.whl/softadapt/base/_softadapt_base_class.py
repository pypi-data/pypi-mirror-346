"""
Implementation of the base class for SoftAdapt.
Copyright (C) 2025 Jacob Logas

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from keras import KerasTensor, backend, ops

from softadapt.utilities._finite_difference import _get_finite_difference


class SoftAdaptBase:
    """Base model for any of the SoftAdapt variants.

    Attributes:
        epsilon: A float which is added to the denominator of a division for
          numerical stability.

    """

    def __init__(self):
        """Initializer of the base method."""
        self.epsilon = backend.epsilon()

    def _softmax(
        self,
        input_tensor: KerasTensor,
        beta: float = 1,
        numerator_weights: KerasTensor | None = None,
        *,
        shift_by_max_value: bool = True,
    ):
        """Implementation of SoftAdapt's modified softmax function.

        Args:
            input_tensor: A tensor of floats which will be used for computing
              the (modified) softmax function.
            beta: A float which is the scaling factor (as described in the
              manuscript).
            numerator_weights: A tensor of weights which are the actual value of
              of the loss components. This option is used for the
              "loss-weighted" variant of SoftAdapt.
            shift_by_max_value: A boolean indicating whether we want the values
              in the input tensor to be shifted by the maximum value.

        Returns:
            A tensor of floats that are the softmax results.

        Raises:
            None.

        """
        if shift_by_max_value:
            exp_of_input = ops.exp(beta * (input_tensor - ops.max(input_tensor)))
        else:
            exp_of_input = ops.exp(beta * input_tensor)

        # This option will be used for the "loss-weighted" variant of SoftAdapt.
        if numerator_weights is not None:
            exp_of_input = ops.multiply(numerator_weights, exp_of_input)

        return exp_of_input / (ops.sum(exp_of_input) + self.epsilon)

    def _compute_rates_of_change(
        self, input_tensor: KerasTensor, order: int = 5, *, verbose: bool = True
    ):
        """Base class method for computing loss functions rate of change.

        Args:
            input_tensor: A tensor of floats containing loss evaluations at the
              previous 'n' points (as many points as the order) of the finite
              difference method.
            order: An integer indicating the order of the finite difference
              method we want to use. The function will use the length of the
              'input_array' array if no values is provided.
            verbose: Whether we want the function to print out information about
              computations or not.

        Returns:
            The approximated derivative as a float value.

        Raises:
            None.

        """
        return _get_finite_difference(
            input_array=ops.convert_to_numpy(input_tensor), order=order, verbose=verbose
        )
