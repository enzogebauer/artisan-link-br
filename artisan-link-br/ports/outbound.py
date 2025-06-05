from abc import ABC, abstractmethod
from core.entities import Product, Order, Review


class ProductRepositoryPort(ABC):
    @abstractmethod
    def save(self, product: Product):
        pass

    @abstractmethod
    def list_all(self) -> list[Product]:
        pass


class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass


class ReviewRepositoryPort(ABC):
    @abstractmethod
    def save(self, review: Review):
        pass
