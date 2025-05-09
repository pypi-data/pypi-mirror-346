import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression as _LinearRegression


class LinearRegression(_LinearRegression):
    def fit(self, X, y, sample_weight=None):
        result = super().fit(X, y, sample_weight)
        self._X = X
        self._y = y
        self._residuals = y - self.predict(X)
        self._n, self._p = X.shape
        X_to_stack = (
            X.values.astype(float) if isinstance(X, pd.DataFrame) else X.astype(float)
        )
        self._X_design = np.hstack([np.ones((self._n, 1)), X_to_stack])
        self._mse = np.sum(self._residuals**2) / (self._n - self._p - 1)
        self._se = np.sqrt(self._mse)
        self._var_names = (
            list(X.columns)
            if hasattr(X, "columns")
            else [f"x{i}" for i in range(1, self._p + 1)]
        )
        return result

    def add_prediction_intervals(
        self, forecast_df: pd.DataFrame, new_X: pd.DataFrame
    ) -> pd.DataFrame:
        if not all(name in new_X.columns for name in self._var_names):
            raise ValueError(
                "new_X must contain the same columns as the training data."
            )

        new_X_np = np.hstack(
            [np.ones((new_X.shape[0], 1)), new_X[self._var_names].values.astype(float)]
        )
        intervals = []
        for x_star in new_X_np:
            _XtX_inv = np.linalg.inv(self._X_design.T @ self._X_design)
            se_pred = np.sqrt(self._mse * (1 + x_star @ _XtX_inv @ x_star.T))
            intervals.append(se_pred)

        intervals = np.array(intervals)
        forecast_df["LinearRegression-lo-95"] = (
            forecast_df["LinearRegression"] - 1.96 * intervals  # type: ignore
        )
        forecast_df["LinearRegression-hi-95"] = (
            forecast_df["LinearRegression"] + 1.96 * intervals  # type: ignore
        )
        forecast_df["LinearRegression-lo-80"] = (
            forecast_df["LinearRegression"] - 1.28 * intervals  # type: ignore
        )
        forecast_df["LinearRegression-hi-80"] = (
            forecast_df["LinearRegression"] + 1.28 * intervals  # type: ignore
        )
        return forecast_df
