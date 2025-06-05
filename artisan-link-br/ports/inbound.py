from abc import ABC, abstractmethod
from typing import List
from core.entities import Product, Order, Review


class ProductServicePort(ABC):
    @abstractmethod
    def list_products(self) -> List[Product]:
        pass

    @abstractmethod
    def add_product(self, product: Product):
        pass


class OrderServicePort(ABC):
    @abstractmethod
    def create_order(self, order: Order):
        pass


class ReviewServicePort(ABC):
    @abstractmethod
    def add_review(self, review: Review):
        pass
