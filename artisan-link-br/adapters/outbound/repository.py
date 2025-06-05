from typing import List
from core.entities import Product, Order, Review
from ports.outbound import (
    ProductRepositoryPort,
    OrderRepositoryPort,
    ReviewRepositoryPort,
)


class ProductRepository(ProductRepositoryPort):
    def __init__(self):
        self._products = []

    def save(self, product: Product):
        self._products.append(product)

    def list_all(self) -> List[Product]:
        return self._products


class OrderRepository(OrderRepositoryPort):
    def __init__(self):
        self._orders = []

    def save(self, order: Order):
        self._orders.append(order)


class ReviewRepository(ReviewRepositoryPort):
    def __init__(self):
        self._reviews = []

    def save(self, review: Review):
        self._reviews.append(review)
