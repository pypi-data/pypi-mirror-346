from abc import ABC, abstractmethod
import numpy as np
import json


class ParamsConverter:
    def __init__(self, params_names: list[str]) -> None:
        self.params_names = params_names

    def to_params(self, named_params: dict[str, float]) -> np.ndarray:
        return np.array([named_params[name] for name in self.params_names])

    def to_named_params(self, params: np.ndarray) -> dict[str, float]:
        return {name: params[i] for i, name in enumerate(self.params_names)}


class DiffEquationModel(ABC):
    params_names = []
    params_converter = ParamsConverter(params_names)

    def __init__(self, params: np.ndarray, *args, **kwargs):
        self.params = params

    @abstractmethod
    def predict(
        self, t: np.ndarray | int, prediction_keys: list[str] | None = None
    ): ...

    @classmethod
    def from_named_params(cls, named_params: dict[str, float]):
        params = cls.params_converter.to_params(named_params)
        return cls(params)

    @classmethod
    def save_model(model: 'DiffEquationModel', path: str):
        params = model.params_converter.to_named_params(model.params)
        with open(path, 'w') as file:
            json.dump(params, file)

    @classmethod
    def load_model(model_cls, path: str):
        with open(path, 'r') as file:
            params = json.load(file)
        return model_cls.from_named_params(params)

    @property
    def named_params(self):
        return self.params_converter.to_named_params(self.params)
