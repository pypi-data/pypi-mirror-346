'''Wrapper classes for SciKit-learn regressors.'''

import numpy as np
from sklearn.linear_model import LinearRegression as sk_linear
from sklearn.ensemble import GradientBoostingRegressor as sk_gb


class GradientBoostingRegressor():
    '''Wrapper class for SciKit-learn gradient boosting regressor.'''

    def __init__(
        self,
        loss="squared_error",
        learning_rate=0.1,
        n_estimators=100,
        subsample=1.0,
        criterion="friedman_mse",
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_depth=3,
        min_impurity_decrease=0.0,
        init=None,
        random_state=None,
        max_features=None,
        alpha=0.9,
        verbose=0,
        max_leaf_nodes=None,
        warm_start=False,
        validation_fraction=0.1,
        n_iter_no_change=None,
        tol=1e-4,
        ccp_alpha=0.0,
        linear_fit_intercept=True,
        linear_copy_X=True,
        linear_n_jobs=None, 
        linear_positive=False
    ):

        self.gb_args={
            'loss': loss,
            'learning_rate': learning_rate,
            'n_estimators': n_estimators,
            'subsample': subsample,
            'criterion': criterion,
            'min_samples_split': min_samples_split,
            'min_samples_leaf': min_samples_leaf,
            'min_weight_fraction_leaf': min_weight_fraction_leaf,
            'max_depth': max_depth,
            'min_impurity_decrease': min_impurity_decrease,
            'init': init,
            'random_state': random_state,
            'max_features': max_features,
            'alpha': alpha,
            'verbose': verbose,
            'max_leaf_nodes': max_leaf_nodes,
            'warm_start': warm_start,
            'validation_fraction': validation_fraction,
            'n_iter_no_change': n_iter_no_change,
            'tol': tol,
            'ccp_alpha': ccp_alpha,
        }

        self.linear_args={
            'fit_intercept': linear_fit_intercept,
            'copy_X': linear_copy_X,
            'n_jobs': linear_n_jobs, 
            'positive': linear_positive
        }

        self.train_feature_mins=None
        self.train_feature_maxes=None

        self.gb_model=sk_gb(**self.gb_args)
        self.linear_model=sk_linear(**self.linear_args)


    def fit(self, X, y, sample_weight=None, monitor=None) -> None:
        '''Compound fit function. Fits SciKit-learn gradient boosting and linear 
        regression models. Also determines label range to be used for prediction
        switching cutoff.'''

        self.train_feature_mins=X.min().to_list()
        self.train_feature_maxes=X.max().to_list()

        self.gb_model.fit(X, y, sample_weight=sample_weight, monitor=monitor)
        self.linear_model.fit(X, y, sample_weight=sample_weight)


    def predict(self, X) -> np.array:
        '''Compound predict method. Returns linear regression results when
        gradient boosting results reach 10th or 90th percentile of label range.'''

        gb_predictions=self.gb_model.predict(X)
        linear_predictions=self.linear_model.predict(X)

        predictions=np.where(
            np.logical_or(
                np.any(X < self.train_feature_mins, axis=1),
                np.any(X > self.train_feature_maxes, axis=1)
            ),
            gb_predictions + (linear_predictions - gb_predictions),
            gb_predictions
        )

        return predictions

