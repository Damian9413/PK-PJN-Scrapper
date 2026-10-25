"""Pure functions that turn raw scraped strings into clean values."""

CURRENCY_SYMBOLS = ["zł", "€", "PLN", "EUR", "pln", "eur"]

def parse_price(raw: str | None) -> float | None:
    if raw is None:
        return None
    text = raw
    for symbols in CURRENCY_SYMBOLS:
        text = text.replace(symbols, "")
    text = text.replace(",",".")
    text = text.replace("\xa0", "")
    text = text.replace(" ", "")
    text = float(text)
    return text

def parse_currency(raw: str | None) -> str | None:
    """'302,10\xa0€' -> 'EUR', '1\xa0389,64\xa0zł' -> 'PLN'."""
    if raw is None:
        return None
    if "€" in raw or "eur" in raw.lower():
        return "EUR"
    return "PLN"

def parse_bool(raw: str | None) -> bool | None:
    """'Tak' -> True, 'Nie' -> False, anything else -> None."""
    if raw is None:
        return None
    return {"tak": True, "nie": False}.get(raw.strip().lower())

def parse_int(raw: str | None) -> int | None:
    """'36 mies.' -> 36, '1385' -> 1385, '' -> None. Keeps only digits."""
    if raw is None:
        return None
    digits = "".join(ch for ch in raw if ch.isdigit())
    return int(digits) if digits else None

def parse_float(raw: str | None) -> float | None:
    """'3.9' -> 3.9, '0.55 kg' -> 0.55. Keeps digits, dot and comma."""
    if raw is None:
        return None
    kept = "".join(ch for ch in raw if ch.isdigit() or ch in ".,")
    return float(kept.replace(",", ".")) if kept else None