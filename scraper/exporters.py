"""Writes cleaned records to files in different formats."""

import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path


class Exporter(ABC):
    """Contract: save a list of records to a file."""

    @abstractmethod
    def export(self, records: list[dict], path: Path) -> None:
        ...


class CsvExporter(Exporter):
    """One row = one record, one column = one attribute."""

    def export(self, records: list[dict], path: Path) -> None:
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)


class JsonExporter(Exporter):
    """A JSON array of objects, human-readable."""

    def export(self, records: list[dict], path: Path) -> None:
        with path.open("w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=2, default=str)