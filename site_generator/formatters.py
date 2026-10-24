"""Presentation helpers used as Jinja filters."""
from datetime import date, timedelta

NBSP = "\u00a0"  # non-breaking space
CURRENCY_SYMBOLS = {"PLN": "zł", "EUR": "€"}


def format_price(value: float, currency: str = "PLN") -> str:

    formatted = f"{value:,.2f}"                     # '1,299.00'
    formatted = formatted.replace(",", NBSP)        # '1 299.00'
    formatted = formatted.replace(".", ",")         # '1 299,00'
    return f"{formatted}{NBSP}{CURRENCY_SYMBOLS[currency]}"

def format_date(value: date, today: date | None = None) -> str:
    """Shows dates in inconsistent formats on purpose."""
    today = today or date.today()
    if value == today - timedelta(days=1):
        return "wczoraj"
    if value.toordinal() % 2 == 0:
        return value.strftime("%d.%m.%Y")   # 26.08.2026
    return value.isoformat()                 # 2026-08-26