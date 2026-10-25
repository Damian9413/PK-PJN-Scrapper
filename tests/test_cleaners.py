"""Unit tests for cleaning functions."""

from datetime import date

from scraper.cleaners import (
    clean_record,
    parse_bool,
    parse_currency,
    parse_date,
    parse_float,
    parse_int,
    parse_price,
)

def test_parse_price_pln_with_thousand_separator():
    assert parse_price("1 000,00 PLN") == 1000.0

def test_parse_price_eur():
    assert parse_price("302,10\xa0€") == 302.1

def test_parse_price_none():
    assert parse_price(None) is None

# --- parse_currency ---

def test_parse_currency_eur():
    assert parse_currency("302,10\xa0€") == "EUR"


def test_parse_currency_pln():
    assert parse_currency("1\xa0389,64\xa0zł") == "PLN"


# --- parse_bool ---

def test_parse_bool_tak():
    assert parse_bool("Tak") is True


def test_parse_bool_nie():
    assert parse_bool("Nie") is False


def test_parse_bool_unknown_value():
    assert parse_bool("Może") is None


# --- parse_int ---

def test_parse_int_with_unit():
    assert parse_int("36 mies.") == 36


def test_parse_int_no_digits():
    assert parse_int("brak") is None


# --- parse_float ---

def test_parse_float_with_unit():
    assert parse_float("0.55 kg") == 0.55


def test_parse_float_comma():
    assert parse_float("3,9") == 3.9

# --- parse_date ---

def test_parse_date_iso():
    assert parse_date("2026-06-14") == date(2026, 6, 14)


def test_parse_date_polish():
    assert parse_date("14.06.2026") == date(2026, 6, 14)


def test_parse_date_yesterday():
    assert parse_date("wczoraj", today=date(2026, 10, 25)) == date(2026, 10, 24)


def test_parse_date_unknown_format():
    assert parse_date("w zeszłym tygodniu") is None


# --- clean_record ---

FULL_RAW_RECORD = {
    "id": "7",
    "name": "Bosch Głośnik 338",
    "price": "2\xa0536,66\xa0zł",
    "category": "Audio",
    "manufacturer": "Bosch",
    "available": "Tak",
    "rating": "4.2",
    "review_count": "120",
    "added_date": "wczoraj",
    "warranty": "24 mies.",
    "description": "Opis.",
    "weight": "1.25 kg",
    "color": "czarny",
    "ean": "0012345678905",
    "country_of_origin": "Polska",
    "shipping_cost": "9,99\xa0zł",
    "delivery_days": "3 dni",
    "seller": "Firma s.c.",
    "detail_url": "http://localhost:8000/product/7.html",
}


def test_clean_record_converts_types():
    clean = clean_record(FULL_RAW_RECORD, today=date(2026, 10, 25))
    assert clean["id"] == 7
    assert clean["price"] == 2536.66
    assert clean["currency"] == "PLN"
    assert clean["available"] is True
    assert clean["added_date"] == date(2026, 10, 24)
    assert clean["warranty_months"] == 24
    assert clean["weight_kg"] == 1.25
    assert clean["shipping_cost"] == 9.99


def test_clean_record_keeps_ean_as_string_with_leading_zeros():
    assert clean_record(FULL_RAW_RECORD)["ean"] == "0012345678905"


def test_clean_record_without_detail_fields_gives_none():
    list_only = {k: v for k, v in FULL_RAW_RECORD.items() if k in ("id", "name", "price")}
    clean = clean_record(list_only)
    assert clean["weight_kg"] is None
    assert clean["shipping_cost"] is None
    assert clean["seller"] is None
    assert clean["detail_url"] is None
