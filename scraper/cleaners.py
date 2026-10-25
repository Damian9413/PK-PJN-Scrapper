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


