"""Renders product lists into HTML using Jinja2 templates."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from site_generator.formatters import format_price
from site_generator.models import Product
from site_generator.paginator import Page

# folder "templates" next to this file, no matter where the script is run from
TEMPLATES_DIR = Path(__file__).parent / "templates"


class HtmlRenderer:
    """Turns products into HTML text. Does not write files."""

    def __init__(self) -> None:
        self._env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        self._env.filters["price"] = format_price

    def render_catalog(self, page: Page) -> str:
        template = self._env.get_template("catalog.html")
        return template.render(page=page)

    def render_index(self, total_pages: int) -> str:
        template = self._env.get_template("index.html")
        return template.render(total_pages=total_pages)

    def render_product(self, product: Product) -> str:
        template = self._env.get_template("product.html")
        return template.render(product=product)