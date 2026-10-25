"""Data quality checks: missing values, column types and outliers."""

import pandas as pd

IQR_FACTOR = 1.5  # Tukey's rule


def missing_values(products: pd.DataFrame) -> pd.DataFrame:
    """Number and percentage of missing values in each column."""
    count = products.isna().sum()
    return pd.DataFrame({"missing": count, "percent": (count / len(products) * 100).round(1)})


def column_types(products: pd.DataFrame) -> pd.Series:
    """pandas dtype of each column."""
    return products.dtypes.astype(str)


def iqr_bounds(values: pd.Series) -> tuple[float, float]:
    """Lower and upper fence: Q1 - 1.5 * IQR and Q3 + 1.5 * IQR."""
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - IQR_FACTOR * iqr, q3 + IQR_FACTOR * iqr


def iqr_outliers(products: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """For each column: fences and the number of values outside them."""
    rows = []
    for column in columns:
        values = products[column].dropna()
        low, high = iqr_bounds(values)
        outside = values[(values < low) | (values > high)]
        rows.append({"column": column, "lower": low, "upper": high, "outliers": len(outside)})
    return pd.DataFrame(rows).set_index("column").round(2)
