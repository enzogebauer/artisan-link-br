from typing import List
from core.entities import Product, Order, Review
from ports.outbound import (
    ProductRepositoryPort,
    OrderRepositoryPort,
    ReviewRepositoryPort,
)


class ProductService:
    def __init__(self, product_repo: ProductRepositoryPort):
        self.product_repo = product_repo

    def list_products(self) -> List[Product]:
        return self.product_repo.list_all()

    def add_product(self, product: Product):
        self.product_repo.save(product)


class OrderService:
    def __init__(self, order_repo: OrderRepositoryPort):
        self.order_repo = order_repo

    def create_order(self, order: Order):
        self.order_repo.save(order)


class ReviewService:
    def __init__(self, review_repo: ReviewRepositoryPort):
        self.review_repo = review_repo

    def add_review(self, review: Review):
        self.review_repo.save(review)
