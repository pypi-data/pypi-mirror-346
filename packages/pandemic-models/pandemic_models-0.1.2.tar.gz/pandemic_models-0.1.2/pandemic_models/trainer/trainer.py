import numpy as np
from pandemic_models.models.base import DiffEquationModel
from pandemic_models.optimizers.base import BaseOptimizer
from pandemic_models.optimizers.objective_functions import BaseObjectiveFunction


class Trainer:
    def __init__(
        self,
        model_cls: type[DiffEquationModel],
        optimizer_cls: type[BaseOptimizer],
        objective_cls: type[BaseObjectiveFunction],
        true_values: dict[str, np.ndarray] | np.ndarray,
        bounds: list[tuple[float, float]],
        metric: str = 'mae',
        prediction_keys: str | list[str] = 'I',
    ):
        """
        Initializes the trainer with a model class, optimizer, and objective function.

        Parameters:
        - `model_cls`: The differential equation model class to train.
        - `optimizer_cls`: The optimizer class to use for parameter optimization.
        - `objective_cls`: The objective function class to compute the loss.
        - `true_values`: Observed data to fit the model to. Can be a dictionary for multi-target or array for single-target.
        - `bounds`: Bounds for the model parameters.
        - `metric`: Metric to evaluate the fit ('mae', 'mse', 'rmse', or a callable).
        - `prediction_keys`: Key(s) to compare predictions against observed data.
        """
        self.model_cls = model_cls
        self.optimizer_cls = optimizer_cls
        self.objective_cls = objective_cls
        self.true_values = true_values
        self.bounds = bounds
        self.metric = metric
        self.prediction_keys = (
            [prediction_keys] if isinstance(prediction_keys, str) else prediction_keys
        )

        self.objective_function = self._initialize_objective_function()

    def _initialize_objective_function(self):
        """
        Initializes the objective function with the appropriate parameters.
        """
        if isinstance(self.true_values, dict):  # Multi-target case
            return self.objective_cls(
                model_cls=self.model_cls,
                true_values=self.true_values,
                metric=self.metric,
            )
        else:  # Single-target case
            return self.objective_cls(
                model_cls=self.model_cls,
                true_values=self.true_values,
                metric=self.metric,
                prediction_keys=self.prediction_keys[0],  # Single target
            )

    def train(self, **optimizer_kwargs):
        """
        Trains the model by optimizing its parameters to fit the observed data.

        Parameters:
        - `optimizer_kwargs`:  Keyword arguments for the optimizer.optimize

        Returns:
        - A dictionary with the optimized parameters and the associated loss.
        """
        optimizer = self.optimizer_cls(self.objective_function)
        optimization_result = optimizer.optimize(bounds=self.bounds, **optimizer_kwargs)
        best_params = optimization_result['best_params']
        best_score = optimization_result['best_score']

        return {
            'best_params': best_params,
            'best_score': best_score,
            'model': self.model_cls(best_params),
        }

    def evaluate(self, params: np.ndarray):
        """
        Evaluates the model with the given parameters against the observed data.

        Parameters:
        - `params`: Model parameters to evaluate.

        Returns:
        - The computed loss based on the objective function.
        """
        return self.objective_function(params)
