"""
Data Models – Dataclass definitions for the core domain entities.

Each dataclass mirrors the corresponding database table schema and is used
for type-safe data passing between the service and presentation layers.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """Represents a single inventory product."""

    id: Optional[int]
    name: str
    category_id: Optional[int]
    warehouse_id: Optional[int]
    rack_number: str
    image_path: Optional[str]
    details: str
    production_date: Optional[str]   # ISO-8601 date string
    expiry_date: Optional[str]       # ISO-8601 date string
    quantity: int
    low_stock_alert: int             # threshold for low-stock warnings
    distributor_price: float         # purchase / cost price
    selling_price: float             # retail price
    model: str
    sku: str                         # Stock Keeping Unit
    supplier_id: Optional[int]
