from dataclasses import dataclass
from datetime import date


@dataclass
class Product:
    # --- fields shown on the list page (table / cards) ---
    id: int
    name: str
    price: float
    category: str
    manufacturer: str
    available: bool
    rating: float| None
    review_count: int | None
    added_date: date
    warranty_months: int | None
    # --- fields shown only on the product detail page ---
    description: str
    weight_kg: float
    color: str
    ean: str
    country_of_origin: str
    shipping_cost: float | None
    delivery_days: int
    seller: str


