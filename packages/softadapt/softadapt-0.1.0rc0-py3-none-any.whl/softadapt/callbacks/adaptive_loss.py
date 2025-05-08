"""
Adaptive loss Keras callback.
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

from typing import Literal

import numpy as np
from keras import KerasTensor, backend, callbacks, ops
from keras.src.utils import file_utils

from softadapt.algorithms import (
    LossWeightedSoftAdapt,
    NormalizedSoftAdapt,
    SoftAdapt,
)


class AdaptiveLossCallback(callbacks.Callback):
    """Keras callback for use of SoftAdapt within the Keras machine learning framework.

    Attributes:
        components (list[str]): _description_
        weights (list[float]): _description_
        frequency (Literal["epoch", "batch"] | int, optional): _description_. Defaults to "epoch".
        beta (float, optional): _description_. Defaults to 0.1.
        accuracy_order (int | None, optional): _description_. Defaults to None.
        algorithm (Literal["loss-weighted", "normalized", "base"], optional): _description_. Defaults to "base".
        backup_dir (str | None, optional): _description_. Defaults to None.
        calculate_on_validation (bool, optional): _description_. Defaults to False.
    """

    def __init__(
        self,
        components: list[str],
        weights: list[float],
        frequency: Literal["epoch", "batch"] | int = "epoch",
        beta: float = 0.1,
        accuracy_order: int | None = None,
        algorithm: Literal["loss-weighted", "normalized", "base"] = "base",
        backup_dir: str | None = None,
        *,
        calculate_on_validation: bool = False,
    ):
        if algorithm == "base":
            self.algorithm = SoftAdapt(beta=beta, accuracy_order=accuracy_order)
        elif algorithm == "loss-weighted":
            self.algorithm = LossWeightedSoftAdapt(
                beta=beta, accuracy_order=accuracy_order
            )
        else:
            self.algorithm = NormalizedSoftAdapt(
                beta=beta, accuracy_order=accuracy_order
            )

        self.frequency = frequency
        self.order = components
        self._weights = weights
        self.components_history: list[KerasTensor] = [[] for _ in components]
        self.debug = False
        self.val = calculate_on_validation
        if backup_dir:
            self.backup_dir = backup_dir
            self._component_history_path = file_utils.join(
                backup_dir, "adaptive_loss_metadata.npy"
            )
            self._adaptive_loss_weights_path = file_utils.join(
                backup_dir, "adaptive_loss_weights.npy"
            )
        else:
            self.backup_dir = None
            self._component_history_path = None

    @property
    def weights(self) -> list[float]:
        return self._weights

    @weights.setter
    def weights(self, value):
        self._weights = value

    def on_train_begin(self, logs: dict | None = None):
        """Get adaptive loss state from temporary file and restore it."""
        if self.backup_dir is not None:
            if file_utils.exists(self._component_history_path):
                saved_history = np.load(self._component_history_path)
                self.components_history = [
                    [ops.convert_to_tensor(i) for i in component]
                    for component in saved_history
                ]
            if file_utils.exists(self._adaptive_loss_weights_path):
                saved_weights = np.load(self._adaptive_loss_weights_path)
                self.weights = ops.convert_to_tensor(saved_weights)
        return super().on_train_begin(logs)

    def on_epoch_end(self, epoch: int, logs: dict | None = None):
        # Update component history in order for weight computation
        if self.val:
            for k in self.order:
                self.components_history[self.order.index(k)].append(
                    ops.copy(logs["val_" + k])
                )
        else:
            for k in self.order:
                self.components_history[self.order.index(k)].append(ops.copy(logs[k]))

        # If the set number of epochs or frequency is met than recompute loss weights
        if (
            (self.frequency == "epoch" or epoch % self.frequency == 0)
            and epoch != 0
            and len(self.components_history[0]) > 1
        ):
            adapt_weights = self.algorithm.get_component_weights(
                *ops.convert_to_tensor(self.components_history, dtype=backend.floatx()),
                verbose=self.debug,
            )

            self.weights = ops.cast(adapt_weights, backend.floatx())

            for h in self.components_history:
                if (
                    self.frequency == "epoch"
                ):  # In the case of an epoch-wise evaluation, the most recent loss value is retained
                    h.pop(0)
                else:
                    h.clear()
        if self.backup_dir is not None:
            if not file_utils.exists(self.backup_dir):
                file_utils.makedirs(self.backup_dir)
            np.save(
                self._adaptive_loss_weights_path, ops.convert_to_numpy(self.weights)
            )
            np.save(
                self._component_history_path,
                np.array(
                    [
                        ops.convert_to_numpy(component)
                        for component in self.components_history
                    ]
                ),
            )
