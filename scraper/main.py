"""Scraper entry point: crawl the catalogue, enrich, clean, export."""
import requests

from scraper.extractors import CatalogPageExtractor, DetailPageExtractor
from bs4 import BeautifulSoup

from scraper.fetcher import Fetcher
from scraper.cleaners import clean_record

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

def enrich_with_details(fetcher: Fetcher, records: list[dict]) -> list[dict]:
    """Fetches each detail page and merges its fields into the record."""
    extractor = DetailPageExtractor()
    enriched = []
    for i, record in enumerate(records, start=1):
        details = {}
        if record["detail_url"] is not None:
            try:
                soup = BeautifulSoup(fetcher.fetch(record["detail_url"]), "lxml")
                details = extractor.extract(soup)
            except requests.RequestException as error:
                print(f"  ! could not fetch {record['detail_url']}: {error}")
        enriched.append({**record, **details})
        if i % 50 == 0:
            print(f"  details: {i}/{len(records)}")
    return enriched


def main() -> None:
    fetcher = Fetcher()
    records = crawl_catalog(fetcher, START_URL)
    print(f"Collected {len(records)} records from the catalogue")
    unique = deduplicate(records)
    print(f"Duplicates removed: {len(records) - len(unique)}, unique records: {len(unique)}")

    full = enrich_with_details(fetcher, unique)
    print(f"Records with details: {len(full)}, fields in first record: {len(full[0])}")

    clean = [clean_record(record) for record in full]
    print(clean[0])


if __name__ == "__main__":
    main()