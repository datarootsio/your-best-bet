import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted
from sklearn.preprocessing import OrdinalEncoder


class SelectTransformer(TransformerMixin, BaseEstimator):
    """This transformer will select and drop columns"""

    def __init__(self, include=None, exclude=[]):
        self.include = include
        self.exclude = exclude

    def validate(self, X):
        if not isinstance(X, pd.DataFrame):
            raise ValueError()

        # X = check_array(X, force_all_finite="allow-nan")

        return X

    def fit(self, X, y=None):
        self.validate(X)
        self.feature_names_in_ = list(X)

        out_cols = (set(X) & set(self.include if self.include else X)) - set(
            self.exclude
        )

        self.feature_names_out_ = list(filter(lambda c: c in out_cols, list(X)))

        return self

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, "feature_names_out_")
        return self.feature_names_out_

    def transform(self, X):
        # Check is fit had been called
        check_is_fitted(self, "feature_names_in_")

        # Input validation
        self.validate(X)

        # Check input
        if len(set(self.feature_names_in_) - set(X)) > 0:
            raise ValueError("Columns seen in fit not in transform")

        if self.include:
            X = X[self.include]

        X = X.drop(columns=self.exclude)

        return X


class GroupedImputer(TransformerMixin, BaseEstimator):
    """This transformer will impute missing data differently based on the group"""

    def __init__(self, groupby, agg_func="mode"):
        self.groupby = groupby
        self.agg_func = agg_func

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, "feature_names_out_")
        return self.feature_names_out_

    def fit(self, X, y=None):
        columns = list(X)
        self.feature_names_in_ = columns
        self.feature_names_out_ = columns

        match self.agg_func:
            case "mode":
                agg_func = pd.Series.mode
            case "mean":
                agg_func = pd.Series.mean
            case "median":
                agg_func = pd.Series.median
            case _:
                agg_func = pd.Series.median

        def mode_map(el):
            if np.isscalar(el) or len(el) == 0:
                return el
            return el[0]

        # there is an exotic scenario where the mode is null -> watch out!
        self.fill_data = (
            X.groupby(self.groupby)
            .agg(agg_func)
            # the mode can be a list => take the first one
            .applymap(mode_map)
            .reset_index()
        )

        return self

    def transform(self, X):
        # Check is fit had been called
        check_is_fitted(self, "fill_data")

        df_merged = X.merge(
            self.fill_data, on=self.groupby, how="left", suffixes=("", "_fill")
        )
        df_merged.index = X.index

        for c in filter(lambda c: c not in self.groupby, self.feature_names_in_):
            df_merged[c] = df_merged[c].fillna(value=df_merged[f"{c}_fill"])

        X_out = df_merged.drop(
            columns=[c for c in df_merged.columns if c.endswith("_fill")]
        )
        return X_out
