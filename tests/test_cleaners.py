"""Unit tests for cleaning functions."""

from datetime import date

from scraper.cleaners import (
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