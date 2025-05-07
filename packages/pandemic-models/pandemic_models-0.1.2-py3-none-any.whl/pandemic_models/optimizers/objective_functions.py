from typing import Callable
import numpy as np
from pandemic_models.models.base import DiffEquationModel


# Metrics
def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean(np.abs(y_true - y_pred))


def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean((y_true - y_pred) ** 2)


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.sqrt(mse(y_true, y_pred))


class BaseObjectiveFunction:
    def __init__(
        self,
        model_cls: DiffEquationModel,
        true_values: np.ndarray | dict[str, np.ndarray],
        metric: str | Callable[[np.ndarray, np.ndarray], float] = 'mae',
        prediction_keys: str | list[str] = 'I',
    ):
        """
        Base class for objective functions.
        - `model_cls`: The model class (e.g., SirModel).
        - `true_values`: Observed/true values for evaluation.
          - For single-target: np.ndarray.
          - For multi-target: dict with keys matching `prediction_keys`.
        - `metric`: Metric to minimize (e.g., "mae", "mse", or a custom callable).
        - `prediction_keys`: Key(s) in the model output to evaluate.
          - Single-target: string (e.g., "I").
          - Multi-target: list of strings (e.g., ["S", "I", "R"]).
        """
        self.model_cls = model_cls
        self.true_values = true_values
        self.prediction_keys = (
            [prediction_keys] if isinstance(prediction_keys, str) else prediction_keys
        )
        self.metric_func = {'mae': mae, 'mse': mse, 'rmse': rmse}.get(metric, metric)

        # Validation
        if isinstance(true_values, dict) and not all(
            key in true_values for key in self.prediction_keys
        ):
            raise ValueError('All prediction keys must be in true_values.')

    def _compute_metric(self, true: np.ndarray, pred: np.ndarray) -> float:
        """Compute the metric for a single pair of true and predicted values."""
        return self.metric_func(true, pred)


class ObjectiveFunction(BaseObjectiveFunction):
    def __call__(self, params: np.ndarray) -> float:
        """
        Compute the objective function value for given parameters.
        """
        model = self.model_cls(params)
        predictions = model.predict(len(self.true_values))

        prediction_key = self.prediction_keys[0]
        predicted_values = predictions[prediction_key]

        return self._compute_metric(self.true_values, predicted_values)


class IncidenceObjectiveFunction(BaseObjectiveFunction):
    def __call__(self, params: np.ndarray) -> float:
        """
        Compute the objective function value for given parameters.
        """
        model = self.model_cls(params)
        preds = model.predict(len(self.true_values) + 1)
        S = preds['S']
        predicted_incidence = S[:-1] - S[1:]
        return self._compute_metric(self.true_values, predicted_incidence)

class IncidenceDeathObjectiveFunction(BaseObjectiveFunction):
    def __call__(self, params: np.ndarray) -> float:
        """
        Compute the objective function value for given parameters.
        """
        model = self.model_cls(params)
        preds = model.predict(len(self.true_values['D']) + 1)
        S = preds['S']
        predicted_incidence = S[:-1] - S[1:]
        D = preds['D']
        predicted_death = D[1:] - D[:-1]

        scores = [self._compute_metric(self.true_values['I'], predicted_incidence),
                 self._compute_metric(self.true_values['D'], predicted_death)]
        self._scores = scores
        return np.mean(scores)


class MultiTargetObjectiveFunction(BaseObjectiveFunction):
    def __call__(self, params: np.ndarray) -> float:
        """
        Compute the multi-target objective function value for given parameters.
        """
        model = self.model_cls(params)
        predictions = model.predict(len(next(iter(self.true_values.values()))))

        # Compute the metric for each key and return the average
        scores = [
            self._compute_metric(self.true_values[key], predictions[key])
            for key in self.prediction_keys
        ]
        self._scores = scores
        return np.mean(scores)
