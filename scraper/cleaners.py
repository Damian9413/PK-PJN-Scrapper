"""Pure functions that turn raw scraped strings into clean values."""

from datetime import date, datetime, timedelta

DATE_FORMATS = ["%Y-%m-%d", "%d.%m.%Y"]

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

def parse_date(raw: str | None, today: date | None = None) -> date | None:
    """'2026-06-14' / '14.06.2026' / 'wczoraj' -> date; unknown -> None."""
    if raw is None:
        return None
    today = today or date.today()
    if raw.strip().lower() == "wczoraj":
        return today - timedelta(days=1)
    for pattern in DATE_FORMATS:
        try:
            return datetime.strptime(raw.strip(), pattern).date()
        except ValueError:
            pass  # this pattern doesn't fit, try the next one
    return None

def clean_record(raw: dict, today: date | None = None) -> dict:
    """Turns one raw scraped record into typed values with final column names."""
    return {
        "id": parse_int(raw.get("id")),
        "name": raw.get("name"),
        "price": parse_price(raw.get("price")),
        "currency": parse_currency(raw.get("price")),
        "category": raw.get("category"),
        "manufacturer": raw.get("manufacturer"),
        "available": parse_bool(raw.get("available")),
        "rating": parse_float(raw.get("rating")),
        "review_count": parse_int(raw.get("review_count")),
        "added_date": parse_date(raw.get("added_date"), today),
        "warranty_months": parse_int(raw.get("warranty")),
        "description": raw.get("description"),
        "weight_kg": parse_float(raw.get("weight")),
        "color": raw.get("color"),
        "ean": raw.get("ean"),
        "country_of_origin": raw.get("country_of_origin"),
        "shipping_cost": parse_price(raw.get("shipping_cost")),
        "delivery_days": parse_int(raw.get("delivery_days")),
        "seller": raw.get("seller"),
        "detail_url": raw.get("detail_url"),
    }