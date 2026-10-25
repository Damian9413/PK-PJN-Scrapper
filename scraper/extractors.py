"""Extracts raw text fields from catalogue and detail pages (no cleaning)."""

from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

# field name -> CSS selector inside one product element
LIST_FIELDS = {
    "name": ".name",
    "price": ".price",
    "category": ".category",
    "manufacturer": ".manufacturer",
    "available": ".available",
    "rating": ".rating",
    "review_count": ".review-count",
    "added_date": ".added-date",
    "warranty": ".warranty",
}

DETAIL_FIELDS = {
    "description": ".description",
    "weight": ".weight",
    "color": ".color",
    "ean": ".ean",
    "country_of_origin": ".country",
    "shipping_cost": ".shipping-cost",
    "delivery_days": ".delivery-days",
    "seller": ".seller",
}

PRODUCT_SELECTOR = ".product[data-id]"
NEXT_PAGE_SELECTOR = "nav.pagination a.next"
DETAIL_LINK_SELECTOR = "a.product-link"


def _text(element: Tag, selector: str) -> str | None:
    """Text of the first match inside element, or None if missing or empty."""
    found = element.select_one(selector)
    if found is None:  # field doesn't exist
        return None
    text = found.get_text(strip=True)  # strip=True removes spaces/newlines at the edges
    if text == "":  # field exists but is empty
        return None
    return text  # field exists and has text


class CatalogPageExtractor:
    """Reads products and the 'next page' link from one catalogue page."""

    def extract_products(self, soup: BeautifulSoup, page_url: str) -> list[dict]:
        products = []
        for element in soup.select(PRODUCT_SELECTOR):
            record = {"id": element["data-id"]}
            for field, selector in LIST_FIELDS.items():
                record[field] = _text(element, selector)

            link = element.select_one(DETAIL_LINK_SELECTOR)
            record["detail_url"] = urljoin(page_url, link["href"]) if link else None

            products.append(record)
        return products

    def next_page_url(self, soup: BeautifulSoup, page_url: str) -> str | None:
        link = soup.select_one(NEXT_PAGE_SELECTOR)
        if link is None:  # last page: no "next" link
            return None
        return urljoin(page_url, link["href"])


class DetailPageExtractor:
    """Reads the extra fields from one product detail page."""

    def extract(self, soup: BeautifulSoup) -> dict:
        record = {}
        for field, selector in DETAIL_FIELDS.items():
            record[field] = _text(soup, selector)
        return record