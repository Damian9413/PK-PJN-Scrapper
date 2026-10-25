"""Loads the scraper output into a pandas DataFrame with correct types."""

import json
from pathlib import Path

import pandas as pd

EUR_RATE = 4.30  # same fixed rate the shop uses; known to the parser from the task
DATE_COLUMNS = ["added_date"]
TEXT_COLUMNS = {"ean": str}  # EAN is an identifier: keep leading zeros


def load_products(path: Path) -> pd.DataFrame:
    """Reads the cleaned CSV; empty cells become NaN."""
    products = pd.read_csv(path, encoding="utf-8-sig", dtype=TEXT_COLUMNS, parse_dates=DATE_COLUMNS)
    return add_price_pln(products)


def add_price_pln(products: pd.DataFrame) -> pd.DataFrame:
    """Adds price_pln so prices in EUR and PLN can be compared."""
    rate = products["currency"].map({"PLN": 1.0, "EUR": EUR_RATE})
    return products.assign(price_pln=(products["price"] * rate).round(2))


def load_run_summary(path: Path) -> dict:
    """Reads the counts saved by the scraper (records before deduplication)."""
    return json.loads(path.read_text(encoding="utf-8"))
