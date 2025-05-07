import numpy as np
import scipy
from .base import DiffEquationModel, ParamsConverter


class SirModel(DiffEquationModel):
    params_names = ['S0', 'I0', 'R0', 'beta', 'gamma']
    params_converter = ParamsConverter(params_names)

    def __init__(self, params: np.ndarray, *args, **kwargs):
        super().__init__(params)

    def _model_ode(self, y, t):
        S, I, R = y
        sir_params = self.params_converter.to_named_params(self.params)

        beta = sir_params['beta']
        gamma = sir_params['gamma']
        N = S + I + R

        dSdt = -beta * I * S / N
        dIdt = beta * I * S / N - gamma * I
        dRdt = gamma * I

        return [dSdt, dIdt, dRdt]

    def predict(self, t: np.ndarray | int, prediction_keys: list[str] | None = None):
        """
        Predicts the values of S, I, R over time.

        Parameters:
        - `t`: Time points (int or array) to predict.
        - `prediction_keys`: Optional list of keys ("S", "I", "R") to include in the output.
          If None, returns all keys.

        Returns:
        - A dictionary of predictions for the specified keys.
        """
        if isinstance(t, int):
            t = np.linspace(0, t, t)

        sir_params = self.params_converter.to_named_params(self.params)
        S0 = sir_params['S0']
        I0 = sir_params['I0']
        R0 = sir_params['R0']

        result = scipy.integrate.odeint(self._model_ode, (S0, I0, R0), t)
        S, I, R = result.T

        # Map results to keys
        full_output = {'S': S, 'I': I, 'R': R}
        if prediction_keys is not None:
            filtered_output = {key: full_output[key] for key in prediction_keys}
            return filtered_output

        return full_output


class DynamicBetaSirModel(SirModel):
    params_names = ['S0', 'I0', 'R0', 'beta_amp', 'beta_delta', 'gamma', 'N']
    params_converter = ParamsConverter(params_names)

    def _model_ode(self, y, t):
        S, I, R = y
        sir_params = self.params_converter.to_named_params(self.params)

        beta_amp = sir_params['beta_amp']
        beta_delta = sir_params['beta_delta']
        gamma = sir_params['gamma']
        N = sir_params['N']

        # Compute dynamic beta
        beta = beta_amp * np.exp(-beta_delta * t)

        dSdt = -beta * I * S / N
        dIdt = beta * I * S / N - gamma * I
        dRdt = gamma * I

        return [dSdt, dIdt, dRdt]
