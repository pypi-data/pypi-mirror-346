"""The function for automatically computing features."""

import pandas as pd
from statsmodels.tsa.stattools import acf, pacf  # type: ignore

from .feature import FEATURE_TYPE_LAG, VALUE_TYPE_INT, Feature
from .non_categorical_numeric_columns import \
    find_non_categorical_numeric_columns


def _sort_acf_vals(acf_vals: list[float]) -> list[int]:
    return [
        lag
        for lag, val in sorted(
            [
                (lag, val)
                for lag, val in enumerate(acf_vals)
                if abs(val) > 0.3 and lag != 0
            ],
            key=lambda x: abs(x[1]),
            reverse=True,
        )[:4]
    ]


def compute(
    df: pd.DataFrame,
    max_lag: int,
) -> list[Feature]:
    """Process the dataframe for determining timeseries features."""
    features = []
    columns = find_non_categorical_numeric_columns(df)
    for column in columns:
        for lag in _sort_acf_vals(
            acf(df[column], nlags=max_lag, fft=False)  # type: ignore
        ) + _sort_acf_vals(pacf(df[column], nlags=max_lag)):  # type: ignore
            new_feature = Feature(
                feature_type=FEATURE_TYPE_LAG,
                columns=[column],
                value1=VALUE_TYPE_INT,
                value2=lag,
            )
            if new_feature in features:
                continue
            features.append(new_feature)
    return features
