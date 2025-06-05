from dataclasses import dataclass
from typing import List

@dataclass
class Artisan:
    id: int
    name: str
    email: str

@dataclass
class Product:
    id: int
    artisan_id: int
    name: str
    description: str
    price: float

@dataclass
class Order:
    id: int
    customer_id: int
    products: List[Product]
    total: float

@dataclass
class Review:
    id: int
    product_id: int
    customer_id: int
    rating: int
    comment: str