---
layout: post
title: "Wrapping a custom model into a sklearn estimator"
tags: python data
summary: Using the sk-learn API for a custom model created with numpy/scipy
date: 2020-02-02 15:32:08:00
---

Following the study about time series done in [a previous post](/blog/2020-01-29-a-time-series-model/), I want to show you a possible solution to bring a hand-made model (with scipy) to production.

The solution I will detail here is based on the sklearn API, that enable to build custom estimators ([documentation](https://scikit-learn.org/stable/developers/develop.html)). The main idea is to create a new class inheriting from `BaseEstimator` and implementing the `fit` and `predict` methods.


## Overall structure

The structure of our new estimator is the following:

```python
from sklearn.base import BaseEstimator 
from sklearn.base import RegressorMixin


class TSEstimatory(BaseEstimator, RegressorMixin):

    def __init__(self, **model_hyper_parameters):
        """
        """
        super().__init__()

    def fit(self, X, Y=None):
        """
        Fit global model on X features to minimize 
        a given function on Y.

        @param X
        @param Y
        """
		# TODO
        return self

    def predict(self, X):
        """
        @param X: features vector the model will be evaluated on
        """
		# TODO
		return None
```

Once fully implemented, we will be able to use it in this way:

```python
model = TSEstimator()
model.fil(x_train, y_train)
y_pred = model.predict(x_test)
```

We will even be able to use this model within all sklearn tools such as `Pipeline` if some data transformation is needed, or `GridSearchCV` to find optimum hyper paramters. It is also very convenient to store some helper functions. For instance, I tend to add a `plot` method to my custom estimators, which makes easier to visualize the results of the training/eesting phases.


## Implementing the fit method

The fit method will run the `scipy` optimizer. We first have to write the function to be minimized. For this, I am just going to copy the code from the previous post on the topic (link in the intro). We first import the necessary packages, define some constants and create some helper functions:


```python
import numpy as np
from scipy import optimize
from sklearn.base import BaseEstimator 
from sklearn.base import RegressorMixin


PURCHASSED_PRICE = 1.5
FRESH_PRICE = 2.5
FROZEN_PRICE = 0.8


def fresh_price(volume):
    return volume * FRESH_PRICE


def frozen_price(volume):
    return volume * FROZEN_PRICE


def fourier_series(t, p=365.25, n=10):
    """
    :pram t: times
    :pram p: seasonality period. p=365.25 for yearly, p=7 for weekly seaonality
    :param n: number of terms in the fourrier serie
    """
    x = 2 * np.pi * np.arange(1, n + 1) / p
    x = x * t[:, None]
    x = np.concatenate((np.cos(x), np.sin(x)), axis=1)
    return x
```

Now we can enter into the interesting part. The content of the function is almost exactly the code of the previous post, except that now the penalty and the number of seasonal components are no more constant parameters but instance members:


```python
class TSEstimatory(BaseEstimator, RegressorMixin):

    def __init__(self, n_seasonal_components=6, **model_hyper_parameters):
        """
        """
        super().__init__()
        self.n_seasonal_components = n_seasonal_components
        # fitted parameters, initialized to None
        self.params_ = None

    # 1. Building the model
	@property
	def penalty(self):
		return 0

    def _seasonality_model(self, t, params):
        x = fourier_series(t, 52, self.n_seasonal_components)
        return x @ params

    def _model(self, t, params):
        trend = params[0] * t + params[1]
        seasonality = self._seasonality_model(t, params[2:self.n_seasonal_components*2+2])
        return trend + seasonality

    # 2. Define the loss function
    def _loss(self, y_obs, y_pred):
        """Compute the dealer gain
    
        :param np.array y_obs: real sales
        :param np.array y_pred: predicted sales = purchasses
        """
        expenses = y_pred * PURCHASSED_PRICE
        return np.where(
            y_obs >= y_pred, 
            # if real sales are above the predicted ones
            # the only gain is the stock price, so y_pred
            expenses + self.penalty - fresh_price(y_pred),
            # if real sales are below the predicted ones
            # we earn the fresh price for the sales of the day + frozen price of the leftover
            expenses - (fresh_price(y_obs) + frozen_price(y_pred - y_obs))
        ).sum()

    # 3. Function to be minimized
    def _f(self, params, *args):
        """Function to minimize = losses for the dealer

        :param args: must contains in that order:
        - data to be fitted (pd.Series)
        - model (function)
        """
        data = self._train_data
        t = data.t
        y_obs = self._train_target
        y_pred = self._model(t, params)
        l = self._loss(y_pred, y_obs)
        return l
    
    def fit(self, X, Y):
        """
        Fit global model on X features to minimize 
        a given function on Y.

        @param X: train dataset (features, N-dim)
        @param Y: train dataset (target, 1-dim)
        """
        self._train_data = X
        self._train_target = Y
        param_initial_values = [-0.001, 1.3] + [0.1, 0.1] * self.n_seasonal_components
        res = optimize.minimize(
            self._f,
            x0=param_initial_values, 
            tol=100,
        )
        if res.success:
            self.params_ = res.x
        return self
```


This model can be use in the following way:

```python
e = TSEstimatory()
e.fit(data, data.y)
```

## Implementing the predict method

Since we saved the fitted paramters into `self.params_`, the predict method is quite simple:

```python
    def predict(self, X):
        return self._model(X, self.params_)
```

Example usage

```python
e.predict(data.t.iloc[-10:])
```


## Final word

As already said, the advantage is that now, our model can be used in conjunction with any other sklearn tools: pipelines, grid search to optimize the hyper parameters (`n_seasonal_components`)... This includes the model persistence tools! Meaning we can dump a fitted `TSEstimator`:

```python
from joblib import dump
e = TSEstimatory()
e.fit(data, data.y)
dump(e, "tsestimator.joblib", compress=0)
```

This dumped file can be read again, for instance in a production environemnt:
```python
from joblib import dump, load
e = load("tsestimator.joblib")
e.predict(...)
```
