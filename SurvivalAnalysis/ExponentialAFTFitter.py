from lifelines.fitters import ParametricRegressionFitter
from autograd import numpy as np
from lifelines.datasets import load_rossi


class ExponentialAFTFitter(ParametricRegressionFitter):

    # this class property is necessary, and should always be a non-empty list of strings.
    _fitted_parameter_names = ['lambda_']

    def _cumulative_hazard(self, params, t, Xs):
        # params is a dictionary that maps unknown parameters to a numpy vector.
        # Xs is a dictionary that maps unknown parameters to a numpy 2d array
        beta = params['lambda_']
        X = Xs['lambda_']
        lambda_ = np.exp(np.dot(X, beta))
        return t / lambda_
