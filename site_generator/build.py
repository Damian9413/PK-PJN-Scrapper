"""Builds the static shop website into the output/ folder."""

from pathlib import Path

from site_generator.factory import ProductFactory
from site_generator.renderer import HtmlRenderer

OUTPUT_DIR = Path("output")


def main() -> None:
    products = ProductFactory(seed=42).create_many(60)

    table_products = products[:30]   # first 30 products
    card_products = products[30:]    # the remaining ones

    renderer = HtmlRenderer()
    html = renderer.render_catalog(table_products, card_products)

    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"Saved {len(products)} products to {OUTPUT_DIR / 'index.html'}")

    product_dir = OUTPUT_DIR / "product"
    product_dir.mkdir(exist_ok=True)

    for product in products:
        page = renderer.render_product(product)
        (product_dir / f"{product.id}.html").write_text(page, encoding="utf-8")
    print(f"Saved {len(products)} detail pages to {product_dir}")


if __name__ == "__main__":
    main()