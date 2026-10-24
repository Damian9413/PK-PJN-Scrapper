"""Product data model (pure data, no logic)."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Product:
    """A single product in the shop catalogue."""

    # --- fields shown on the list page (table / cards) ---
    id: int
    name: str
    price: float
    category: str
    manufacturer: str
    available: bool
    rating: float | None  # may be missing (MissingValuesDistorter)
    review_count: int
    added_date: date
    warranty_months: int

    # --- fields shown only on the product detail page ---
    description: str
    weight_kg: float
    color: str
    ean: str  
    country_of_origin: str
    shipping_cost: float | None  # may be missing (MissingValuesDistorter)
    delivery_days: int
    seller: str

    # --- fields with defaults must come last ---
    currency: str = "PLN"