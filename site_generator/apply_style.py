"""
WYGENEROWANE PRZEZ AI (Claude) – nie pisane ręcznie.

Dokleja arkusz stylów do już zbudowanych stron katalogu, bez ruszania
szablonów ani build.py. Uruchamiać PO build.py:

    python -m site_generator.build
    python -m site_generator.apply_style
"""

import shutil
from pathlib import Path

OUTPUT_DIR = Path("output")
CSS_SOURCE = Path(__file__).parent / "static" / "catalog.css"
CSS_NAME = "catalog.css"
LINK_TAG = f'<link rel="stylesheet" href="{CSS_NAME}">'


def main() -> None:
    shutil.copy(CSS_SOURCE, OUTPUT_DIR / CSS_NAME)

    pages = sorted(OUTPUT_DIR.glob("page-*.html"))
    for path in pages:
        html = path.read_text(encoding="utf-8")
        if LINK_TAG in html:
            continue
        html = html.replace("</head>", f"    {LINK_TAG}\n</head>", 1)
        path.write_text(html, encoding="utf-8")

    print(f"Styled {len(pages)} catalog pages.")


if __name__ == "__main__":
    main()
