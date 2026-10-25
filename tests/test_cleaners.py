"""Unit tests for cleaning functions."""

from scraper.cleaners import parse_price

def test_parse_price_pln_with_thousand_separator():
    assert parse_price("1 000,00 PLN") == 1000.0

def test_parse_price_eur():
    assert parse_price("302,10\xa0€") == 302.1

def test_parse_price_none():
    assert parse_price(None) is None