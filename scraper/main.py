"""Scraper entry point: crawl the catalogue, enrich, clean, export."""

from bs4 import BeautifulSoup

from scraper.extractors import CatalogPageExtractor
from scraper.fetcher import Fetcher

START_URL = "http://localhost:8000/page-1.html"


def crawl_catalog(fetcher: Fetcher, start_url: str) -> list[dict]:
    """Follows 'next' links from start_url and collects raw list records."""
    extractor = CatalogPageExtractor()
    records = []
    url = start_url
    while url is not None:
        soup = BeautifulSoup(fetcher.fetch(url), "lxml")
        records.extend(extractor.extract_products(soup, url))
        url = extractor.next_page_url(soup, url)
    return records

def deduplicate(records: list[dict]) -> list[dict]:
    """Keeps the first occurrence of each id."""
    seen = set()
    unique = []
    for record in records:
        if record["id"] in seen:
            continue  # duplicate: skip to the next record
        seen.add(record["id"])
        unique.append(record)
    return unique


def main() -> None:
    fetcher = Fetcher()
    records = crawl_catalog(fetcher, START_URL)
    print(f"Collected {len(records)} records from the catalogue")
    unique = deduplicate(records)
    print(f"Duplicates removed: {len(records) - len(unique)}, unique records: {len(unique)}")


if __name__ == "__main__":
    main()