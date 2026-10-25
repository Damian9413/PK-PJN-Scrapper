"""Descriptive statistics for numeric columns."""

import pandas as pd


def describe(products: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Mean, median, mode (with its count), quartiles, min and max."""
    rows = {}
    for column in columns:
        values = products[column].dropna()
        mode = values.mode().iloc[0]  # smallest of the most frequent values
        rows[column] = {
            "count": len(values),
            "mean": values.mean(),
            "median": values.median(),
            "mode": mode,
            "mode_count": int((values == mode).sum()),
            "q1": values.quantile(0.25),
            "q3": values.quantile(0.75),
            "min": values.min(),
            "max": values.max(),
        }
    return pd.DataFrame(rows).T.round(2)
