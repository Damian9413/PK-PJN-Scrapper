"""Analysis entry point: quality checks, statistics and charts for scraped data."""

from pathlib import Path

import numpy as np
import pandas as pd

from analysis import plots
from analysis.loader import load_products, load_run_summary
from analysis.quality import column_types, iqr_outliers, missing_values
from analysis.statistics import describe

DATA_DIR = Path("data")
PRODUCTS_FILE = DATA_DIR / "products.csv"
RUN_SUMMARY_FILE = DATA_DIR / "run_summary.json"
FIGURES_DIR = Path("reports") / "figures"

NUMERIC_COLUMNS = [
    "price",
    "price_pln",
    "rating",
    "review_count",
    "warranty_months",
    "weight_kg",
    "shipping_cost",
    "delivery_days",
]
# "price" is left out: it mixes two currencies, price_pln is the comparable one
CORRELATION_COLUMNS = [c for c in NUMERIC_COLUMNS if c != "price"]
STRONG_CORRELATION = 0.3


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def strongest_pairs(correlation: pd.DataFrame) -> pd.Series:
    """Off-diagonal pairs sorted by absolute correlation, each pair once."""
    upper_triangle = np.triu(np.ones(correlation.shape, dtype=bool), k=1)
    pairs = correlation.where(upper_triangle).stack()
    return pairs.reindex(pairs.abs().sort_values(ascending=False).index)


def main() -> None:
    pd.set_option("display.width", 120)
    products = load_products(PRODUCTS_FILE)
    summary = load_run_summary(RUN_SUMMARY_FILE)

    section("Records")
    print(f"Collected from catalogue (with duplicates): {summary['collected']}")
    print(f"Duplicates removed by id:                   {summary['duplicates_removed']}")
    print(f"Records after deduplication:                {summary['unique']}")
    print(f"Records in products.csv:                    {len(products)}")
    print(f"Duplicate ids left in CSV:                  {products['id'].duplicated().sum()}")

    section("Missing values per column")
    print(missing_values(products).to_string())

    section("Column types")
    print(column_types(products).to_string())

    section("Currency")
    print(products["currency"].value_counts().to_string())

    section("Outliers (IQR rule)")
    print(iqr_outliers(products, NUMERIC_COLUMNS).to_string())
    by_currency = products.groupby("currency")["price"].agg(["count", "mean", "median", "min", "max"])
    print("\nRaw price by currency:")
    print(by_currency.round(2).to_string())

    section("Descriptive statistics")
    print(describe(products, NUMERIC_COLUMNS).to_string())

    section("Correlation (Pearson)")
    correlation = products[CORRELATION_COLUMNS].corr()
    print(correlation.round(2).to_string())
    pairs = strongest_pairs(correlation)
    print("\nStrongest pairs:")
    print(pairs.head(5).round(3).to_string())
    strong = pairs[pairs.abs() >= STRONG_CORRELATION]
    print(f"Pairs with |r| >= {STRONG_CORRELATION}: {len(strong)}")

    section("Figures")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    saved = [
        plots.histogram(products, "price_pln", 20, FIGURES_DIR / "hist_price_pln.png"),
        plots.histogram(products, "rating", 20, FIGURES_DIR / "hist_rating.png"),
        plots.boxplot_by(products, "price", "currency", FIGURES_DIR / "boxplot_price_by_currency.png"),
        plots.boxplot_by(products, "price_pln", "category", FIGURES_DIR / "boxplot_price_pln_by_category.png"),
        plots.correlation_heatmap(correlation, FIGURES_DIR / "correlation_matrix.png"),
    ]
    for path in saved:
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
