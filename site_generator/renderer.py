"""Renders product lists into HTML using Jinja2 templates."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from site_generator.models import Product

# folder "templates" next to this file, no matter where the script is run from
TEMPLATES_DIR = Path(__file__).parent / "templates"


class HtmlRenderer:
    """Turns products into HTML text. Does not write files."""

    def __init__(self) -> None:
        self._env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def render_catalog(
        self, table_products: list[Product], card_products: list[Product]
    ) -> str:
        template = self._env.get_template("catalog.html")
        return template.render(
            table_products=table_products,
            card_products=card_products,
        )