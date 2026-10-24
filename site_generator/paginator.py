import math
from dataclasses import dataclass

from site_generator.models import Product


@dataclass
class Page:
    """One catalogue sub-page"""

    number: int
    total_pages: int
    table_products: list[Product]
    card_products: list[Product]

class Paginator:
    """Decides how to split products into pages"""

    def __init__(self, page_size: int = 40) -> None:
        self._page_size = page_size

    def paginate(self, products: list[Product]) -> list[Page]:
        total_pages = math.ceil(len(products) / self._page_size)
        pages = []
        for n in range(1, total_pages+1):
            start = (n-1) * self._page_size
            end = start + self._page_size
            chunk = products[start:end]
            half = len(chunk) //2
            pages.append(
                Page(
                    number=n,
                    total_pages=total_pages,
                    table_products=chunk[:half],
                    card_products=chunk[half:],
                )
            )
        return pages
