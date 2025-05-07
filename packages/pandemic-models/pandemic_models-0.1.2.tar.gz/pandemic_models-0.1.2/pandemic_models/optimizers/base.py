from typing import Callable, Any
import numpy as np
from abc import ABC


class BaseOptimizer(ABC):
    """
    Base class for all optimizers.
    """

    def __init__(self, objective_function: Callable[[np.ndarray], float]):
        self.objective_function = objective_function

    def optimize(
        self, bounds: list[tuple[float, float]], *args, **kwargs
    ) -> dict[str, Any]:
        """
        Optimize the objective function within the given bounds.
        Must be implemented by subclasses.
        """
        raise NotImplementedError('Subclasses must implement this method.')
