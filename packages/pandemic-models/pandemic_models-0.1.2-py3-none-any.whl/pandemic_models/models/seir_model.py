import numpy as np
import scipy
from .base import DiffEquationModel, ParamsConverter


class SeirModel(DiffEquationModel):
    params_names = ['S0', 'E0', 'I0', 'R0', 'beta', 'gamma', 'sigma']
    params_converter = ParamsConverter(params_names)

    def __init__(self, params: np.ndarray, *args, **kwargs):
        super().__init__(params)

    def _model_ode(self, y, t):
        S, E, I, R = y
        seir_params = self.params_converter.to_named_params(self.params)

        beta = seir_params['beta']
        gamma = seir_params['gamma']
        sigma = seir_params['sigma']
        N = S + E + I + R

        dSdt = -beta * I * S / N
        dEdt = beta * I * S / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I

        return [dSdt, dEdt, dIdt, dRdt]

    def predict(self, t: np.ndarray | int, prediction_keys: list[str] | None = None):
        """
        Predicts the values of S, E, I, R over time.

        Parameters:
        - `t`: Time points (int or array) to predict.
        - `prediction_keys`: Optional list of keys ("S", "I", "E", "R") to include in the output.
          If None, returns all keys.

        Returns:
        - A dictionary of predictions for the specified keys.
        """
        if isinstance(t, int):
            t = np.linspace(0, t, t)

        seir_params = self.params_converter.to_named_params(self.params)
        S0 = seir_params['S0']
        E0 = seir_params['E0']
        I0 = seir_params['I0']
        R0 = seir_params['R0']

        result = scipy.integrate.odeint(self._model_ode, (S0, E0, I0, R0), t)
        S, E, I, R = result.T

        # Map results to keys
        full_output = {'S': S, 'E': E, 'I': I, 'R': R}
        if prediction_keys is not None:
            filtered_output = {key: full_output[key] for key in prediction_keys}
            return filtered_output

        return full_output
