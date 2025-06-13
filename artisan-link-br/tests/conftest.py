import pytest
from adapters.outbound.repository import ProductRepository, OrderRepository, ReviewRepository
from core.services import ProductService, OrderService, ReviewService

@pytest.fixture
def product_repository():
    return ProductRepository()

@pytest.fixture
def order_repository():
    return OrderRepository()

@pytest.fixture
def review_repository():
    return ReviewRepository()

@pytest.fixture
def product_service(product_repository):
    return ProductService(product_repository)

@pytest.fixture
def order_service(order_repository):
    return OrderService(order_repository)

@pytest.fixture
def review_service(review_repository):
    return ReviewService(review_repository)
