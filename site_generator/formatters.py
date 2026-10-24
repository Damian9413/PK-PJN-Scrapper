"""Presentation helpers used as Jinja filters."""

NBSP = "\u00a0"  # non-breaking space
CURRENCY_SYMBOLS = {"PLN": "zł", "EUR": "€"}


def format_price(value: float, currency: str = "PLN") -> str:

    formatted = f"{value:,.2f}"                     # '1,299.00'
    formatted = formatted.replace(",", NBSP)        # '1 299.00'
    formatted = formatted.replace(".", ",")         # '1 299,00'
    return f"{formatted}{NBSP}{CURRENCY_SYMBOLS[currency]}"