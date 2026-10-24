"""Deliberate data 'damage' that makes the site harder to scrape."""

import math
import random
from abc import ABC, abstractmethod
from dataclasses import replace

from site_generator.models import Product


class Distorter(ABC):
    """Contract: takes products, returns (possibly damaged) products."""

    @abstractmethod
    def apply(self, products: list[Product]) -> list[Product]:
        ...


class MissingValuesDistorter(Distorter):
    """Removes values from chosen fields in a fraction of products."""

    def __init__(self, fields: list[str], fraction: float, seed: int = 42) -> None:
        self._fields = fields
        self._fraction = fraction
        self._random = random.Random(seed)

    def apply(self, products: list[Product]) -> list[Product]:
        for field in self._fields:
            count = math.ceil(len(products) * self._fraction)
            ids_to_clear = set(self._random.sample([p.id for p in products], count))
            products = [
                replace(p, **{field: None}) if p.id in ids_to_clear else p
                for p in products
            ]
        return products
