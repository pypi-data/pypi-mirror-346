import numpy as np
import scipy
from .base import DiffEquationModel, ParamsConverter


class SirdModel(DiffEquationModel):
    params_names = ['S0', 'I0', 'R0', 'D0', 'beta', 'gamma', 'mu', 'N']
    params_converter = ParamsConverter(params_names)

    def __init__(self, params: np.ndarray, *args, **kwargs):
        super().__init__(params)

    def _model_ode(self, y, t):
        S, I, R, D = y
        sird_params = self.params_converter.to_named_params(self.params)

        beta = sird_params['beta']
        gamma = sird_params['gamma']
        mu = sird_params['mu']
        N = sird_params['N']

        dSdt = -beta * I * S / N
        dIdt = beta * I * S / N - gamma * I - mu * I
        dRdt = gamma * I
        dDdt = mu * I

        return [dSdt, dIdt, dRdt, dDdt]

    def predict(self, t: np.ndarray | int, prediction_keys: list[str] | None = None):
        """
        Predicts the values of S, I, R, D over time.

        Parameters:
        - `t`: Time points (int or array) to predict.
        - `prediction_keys`: Optional list of keys ("S", "I", "R", "D") to include in the output.
          If None, returns all keys.

        Returns:
        - A dictionary of predictions for the specified keys.
        """
        if isinstance(t, int):
            t = np.linspace(0, t, t)

        sird_params = self.params_converter.to_named_params(self.params)
        S0 = sird_params['S0']
        I0 = sird_params['I0']
        R0 = sird_params['R0']
        D0 = sird_params['D0']

        result = scipy.integrate.odeint(self._model_ode, (S0, I0, R0, D0), t)
        S, I, R, D = result.T

        # Map results to keys
        full_output = {'S': S, 'I': I, 'R': R, 'D': D}
        if prediction_keys is not None:
            filtered_output = {key: full_output[key] for key in prediction_keys}
            return filtered_output

        return full_output
