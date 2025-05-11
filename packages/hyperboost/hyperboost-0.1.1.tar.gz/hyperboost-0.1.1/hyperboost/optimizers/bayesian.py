import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from scipy.optimize import minimize
from hyperboost.utils.visual import plot_convergence


class BayesianOptimizer:
    def __init__(self, space, objective_func, n_initial_points=5):
        self.model = None
        self.space = space
        self.objective_func = objective_func
        self.n_initial_points = n_initial_points
        self.X = []
        self.y = []
        self.history = []
        self._initialize()

    def _initialize(self):
        initial_points = self.space.sample(self.n_initial_points)
        for point in initial_points:
            loss = self.objective_func(point)
            self.X.append(self.space.transform(point))
            self.y.append(loss)
            self.history.append(loss)

    def _acquisition(self, x, kappa=2.0):
        mu, sigma = self.model.predict([x], return_std=True)
        mu = mu[0]
        sigma = sigma[0]
        return mu - kappa * sigma

    def _optimize_acquisition(self):
        best_x = None
        best_score = float('inf')
        bounds = [(0.0, 1.0)] * len(self.space.param_names)
        for _ in range(20):
            x0 = np.random.rand(len(bounds))
            res = minimize(lambda x: self._acquisition(x), x0=x0, bounds=bounds)
            if res.fun < best_score:
                best_score = res.fun
                best_x = res.x
        return best_x

    def optimize(self, n_iter=30):
        kernel = Matern(nu=2.5)
        self.model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
        for _ in range(n_iter):
            self.model.fit(self.X, self.y)
            next_point = self._optimize_acquisition()
            params = self.space.inverse_transform(next_point)
            loss = self.objective_func(params)
            self.X.append(next_point)
            self.y.append(loss)
            self.history.append(loss)
        best_idx = np.argmin(self.y)
        plot_convergence(self.history)
        return self.space.inverse_transform(self.X[best_idx])
    