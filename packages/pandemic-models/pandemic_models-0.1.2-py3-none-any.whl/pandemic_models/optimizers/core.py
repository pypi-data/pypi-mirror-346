from typing import Callable, Any
import numpy as np
import scipy.optimize
from geneticalgorithm import geneticalgorithm as ga
from pyswarm import pso
import itertools
from .base import BaseOptimizer


class MinimizeOptimizer(BaseOptimizer):
    def optimize(
        self, bounds: list[tuple[float, float]], max_iter: int = 10000, **kwargs
    ) -> dict[str, Any]:
        initial_guess = [np.mean(b) for b in bounds]
        result = scipy.optimize.minimize(
            self.objective_function,
            initial_guess,
            bounds=bounds,
            options={'maxiter': max_iter, 'disp': True},
            **kwargs,
        )
        return {'best_params': result.x, 'best_score': result.fun}


class DifferentialEvolutionOptimizer(BaseOptimizer):
    def optimize(
        self, bounds: list[tuple[float, float]], max_iter: int = 1000, **kwargs
    ) -> dict[str, Any]:
        result = scipy.optimize.differential_evolution(
            self.objective_function, bounds, maxiter=max_iter, **kwargs
        )
        return {'best_params': result.x, 'best_score': result.fun}


class DualAnnealingOptimizer(BaseOptimizer):
    def optimize(
        self,
        bounds: list[tuple[float, float]],
        max_iter: int = 1000,
        seed: int = 0,
        **kwargs
    ) -> dict[str, Any]:
        result = scipy.optimize.dual_annealing(
            self.objective_function, bounds, maxiter=max_iter, seed=seed, **kwargs
        )
        return {'best_params': result.x, 'best_score': result.fun}


class GeneticAlgorithmOptimizer(BaseOptimizer):
    def __init__(self, objective_function: Callable[[np.ndarray], float]):
        super().__init__(objective_function)

    def optimize(
        self, bounds: list[tuple[float, float]], max_iter: int = 1000, **kwargs
    ) -> dict[str, Any]:

        algorithm_parameters = {
            'max_num_iteration': max_iter,
            'population_size': 15,
            'mutation_probability': 0.1,
            'elit_ratio': 0.01,
            'crossover_probability': 0.5,
            'parents_portion': 0.3,
            'crossover_type': 'uniform',
            'max_iteration_without_improv': None,
        }
        algorithm_parameters.update(kwargs)
        model = ga(
            function=self.objective_function,
            dimension=len(bounds),
            variable_type='real',
            variable_boundaries=np.array(bounds),
            convergence_curve=False,
            algorithm_parameters=algorithm_parameters,
        )
        model.run()
        return {
            'best_params': model.output_dict['variable'],
            'best_score': model.output_dict['function'],
        }


class SwarmOptimizer(BaseOptimizer):
    def optimize(
        self, bounds: list[tuple[float, float]], max_iter: int = 200, **kwargs
    ) -> dict[str, Any]:
        lb, ub = zip(*bounds)
        best_params, best_score = pso(
            self.objective_function, lb, ub, swarmsize=100, maxiter=max_iter, **kwargs
        )
        return {'best_params': best_params, 'best_score': best_score}


class GridSearchOptimizer(BaseOptimizer):
    def optimize(
        self, bounds: list[tuple[float, float]], grid_points: int = 5
    ) -> dict[str, Any]:
        param_grid = [np.linspace(low, high, grid_points) for low, high in bounds]
        best_params, best_score = None, float('inf')
        for params in itertools.product(*param_grid):
            score = self.objective_function(np.array(params))
            if score < best_score:
                best_params, best_score = params, score
        return {'best_params': best_params, 'best_score': best_score}
