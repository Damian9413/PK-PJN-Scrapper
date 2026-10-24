"""Generates random products for the catalogue."""

import random
from datetime import date

from faker import Faker

from site_generator.models import Product

CATEGORIES = {
    "Audio": ["Głośnik", "Słuchawki", "Soundbar"],
    "Komputery": ["Laptop", "Desktop", "Tablet", "Monitor", "Myszka"],
    "AGD": ["Czajnik", "Odkurzacz", "Mikser"],
}
MANUFACTURERS = ["Apple", "Samsung","Philips", "Bosch", "Lenovo", "Asus", "HP", "Dell"]
COLORS = ["czarny", "biały", "srebrny", "szary", "czerwony", "niebieski"]
COUNTRIES = ["Chiny", "Niemcy", "Polska", "Wietnam", "Japonia", "Korea Południowa"]
WARRANTY_OPTIONS = [12, 24, 36]
SHIPPING_OPTIONS = [0.0, 9.99, 14.99, 19.99]  # 0.0 = free shipping


class ProductFactory:
    """Creates Product objects with reproducible random data"""

    def __init__(self, seed: int = 42) -> None:
        self._random = random.Random(seed)
        self._faker = Faker("pl_PL")
        self._faker.seed_instance(seed)

    def create(self, product_id: int) -> Product:
        category = self._random.choice(list(CATEGORIES))
        noun = self._random.choice(CATEGORIES[category])
        manufacturer = self._random.choice(MANUFACTURERS)


        return Product(
            id=product_id,
            name=f"{manufacturer} {noun} {self._random.randint(100, 999)}",
            price=round(self._random.uniform(19.99, 4999.99),2),
            category=category,
            manufacturer=manufacturer,
            available=self._random.random() < 0.8,
            rating=round(self._random.uniform(1, 5), 1),
            review_count=self._random.randint(0, 2000),
            added_date=self._faker.date_between(start_date="-1y", end_date="today"),
            warranty_months=self._random.choice(WARRANTY_OPTIONS),
            description=self._faker.paragraph(nb_sentences=3),
            weight_kg=round(self._random.uniform(0.1, 15.0), 2),
            color=self._random.choice(COLORS),
            ean=self._faker.ean13(),
            country_of_origin=self._random.choice(COUNTRIES),
            shipping_cost=self._random.choice(SHIPPING_OPTIONS),
            delivery_days=self._random.randint(1, 7),
            seller=self._faker.company(),
        )

    def create_many(self, count: int) -> list[Product]:
        result = []
        for i in range(1, count + 1):
            result.append(self.create(i))
        return result

