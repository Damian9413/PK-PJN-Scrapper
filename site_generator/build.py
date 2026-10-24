"""Builds the static shop website into the output/ folder."""

from pathlib import Path

from site_generator.distorters import (
    CurrencyDistorter,
    DuplicateDistorter,
    MissingValuesDistorter,
    RecentDateDistorter,
)
from site_generator.factory import ProductFactory
from site_generator.paginator import Paginator
from site_generator.renderer import HtmlRenderer

OUTPUT_DIR = Path("output")
PRODUCT_COUNT = 200
PAGE_SIZE = 40


def main() -> None:
    products = ProductFactory(seed=42).create_many(PRODUCT_COUNT)

    distorters = [
        MissingValuesDistorter(fields=["rating", "shipping_cost"], fraction=0.2),
        CurrencyDistorter(fraction=0.1),
        RecentDateDistorter(fraction=0.05),
        DuplicateDistorter(count=8, source_limit=160),   # always last!
    ]
    for distorter in distorters:
        products = distorter.apply(products)

    pages = Paginator(page_size=PAGE_SIZE).paginate(products)
    renderer = HtmlRenderer()

    OUTPUT_DIR.mkdir(exist_ok=True)
    product_dir = OUTPUT_DIR / "product"
    product_dir.mkdir(exist_ok=True)

    (OUTPUT_DIR / "index.html").write_text(
        renderer.render_index(len(pages)), encoding="utf-8"
    )

    for page in pages:
        html = renderer.render_catalog(page)
        (OUTPUT_DIR / f"page-{page.number}.html").write_text(html, encoding="utf-8")

    for product in products:
        html = renderer.render_product(product)
        (product_dir / f"{product.id}.html").write_text(html, encoding="utf-8")

    print(f"Saved {len(products)} products on {len(pages)} pages + detail pages.")


if __name__ == "__main__":
    main()