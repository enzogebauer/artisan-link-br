from dataclasses import dataclass
from typing import List


@dataclass
class Artisan:
    id: int
    name: str
    email: str


from dataclasses import dataclass, field
from typing import List


@dataclass
class Product:
    id: int
    artisan_id: int
    name: str
    description: str
    price: float = field(default=0.0)

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("O preço do produto deve ser positivo.")


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

    def __post_init__(self):
        if not (1 <= self.rating <= 5):
            raise ValueError("A nota deve estar entre 1 e 5.")
