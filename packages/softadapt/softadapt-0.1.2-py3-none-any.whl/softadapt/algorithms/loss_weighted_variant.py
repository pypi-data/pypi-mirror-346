"""
Implementation of the loss-weighted variant of SoftAdapt.
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

import warnings

from keras import KerasTensor, backend, ops

from softadapt.base._softadapt_base_class import SoftAdaptBase


class LossWeightedSoftAdapt(SoftAdaptBase):
    """Class implementation of the loss-weighted SoftAdapt variant.

    The loss-weighted variant of SoftAdapt is described in section 3.1.1 of our
    manuscript (located at: https://arxiv.org/pdf/1912.12355.pdf).

    Attributes:
        beta: A float that is the 'beta' hyperparameter in our manuscript. If
          beta > 0, then softAdapt will pay more attention the worst performing
          loss component. If beta < 0, then SoftAdapt will assign higher weights
          to the better performing components. Beta==0 is the trivial case and
          all loss components will have coefficient 1.

        accuracy_order: An integer indicating the accuracy order of the finite
          volume approximation of each loss component's slope.
    """

    def __init__(self, beta: float = 0.1, accuracy_order: int | None = None):
        """SoftAdapt class initializer."""
        super().__init__()
        self.beta = beta
        # Passing "None" as the order of accuracy sets the highest possible
        # accuracy in the finite difference approximation.
        self.accuracy_order = accuracy_order

    def get_component_weights(
        self, *loss_component_values: tuple[KerasTensor], verbose: bool = True
    ):
        """Class method for SoftAdapt weights.

        Args:
            loss_component_values: A tuple consisting of the values of the each
              loss component that have been stored for the past 'n' iterations
              or epochs (as described in the manuscript).
            verbose: A boolean indicating user preference for whether internal
              functions should print out information and warning about
              computations.
        Returns:
            The computed weights for each loss components. For example, if there
            were 5 loss components, say (l_1, l_2, l_3, l_4, l_5), then the
            return tensor will be the weights (alpha_1, alpha_2, alpha_3,
            alpha_4, alpha_5) in the order of the loss components.

        Raises:
            None.

        """
        if len(loss_component_values) == 1:
            warnings.warn(
                "You have only passed on the values of one loss component, which will result in trivial weighting.",
                stacklevel=2,
            )

        rates_of_change = []
        average_loss_values = []

        for loss_points in loss_component_values:
            # Compute the rates of change for each one of the loss components.
            rates_of_change.append(
                self._compute_rates_of_change(
                    loss_points, self.accuracy_order, verbose=verbose
                )
            )
            average_loss_values.append(
                ops.mean(ops.cast(loss_points, dtype=backend.floatx()))
            )

        rates_of_change = ops.convert_to_tensor(rates_of_change, dtype=backend.floatx())
        average_loss_values = ops.convert_to_tensor(
            average_loss_values, dtype=backend.floatx()
        )
        # Calculate the weight and return the values.
        return self._softmax(
            input_tensor=rates_of_change,
            beta=self.beta,
            numerator_weights=average_loss_values,
        )
