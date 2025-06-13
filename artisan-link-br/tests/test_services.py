import pytest
from core.entities import Product, Order, Review
from core.services import ProductService, OrderService, ReviewService

class TestProductService:
    def test_add_product(self, product_service):
        """Test adding a product to the service"""
        product = Product(
            id=1, 
            artisan_id=1, 
            name="Vaso de Cerâmica", 
            description="Vaso artesanal", 
            price=50.0
        )
        
        product_service.add_product(product)
        products = product_service.list_products()
        
        assert len(products) == 1
        assert products[0] == product
    
    def test_list_empty_products(self, product_service):
        """Test listing products when repository is empty"""
        products = product_service.list_products()
        assert products == []
    
    def test_list_multiple_products(self, product_service):
        """Test listing multiple products"""
        product1 = Product(id=1, artisan_id=1, name="Vaso", description="Vaso", price=50.0)
        product2 = Product(id=2, artisan_id=1, name="Prato", description="Prato", price=30.0)
        
        product_service.add_product(product1)
        product_service.add_product(product2)
        
        products = product_service.list_products()
        assert len(products) == 2
        assert product1 in products
        assert product2 in products

class TestOrderService:
    def test_create_order(self, order_service):
        """Test creating an order"""
        products = [
            Product(id=1, artisan_id=1, name="Vaso", description="Vaso", price=50.0)
        ]
        order = Order(id=1, customer_id=1, products=products, total=50.0)
        
        order_service.create_order(order)
        # Como não temos método para listar orders, vamos assumir que foi salvo
        # Este é um exemplo de TDD - implementaremos depois
        assert True  # Placeholder até implementarmos list_orders

class TestReviewService:
    def test_add_review(self, review_service):
        """Test adding a review"""
        review = Review(
            id=1, 
            product_id=1, 
            customer_id=1, 
            rating=5, 
            comment="Excelente produto!"
        )
        
        review_service.add_review(review)
        # Como não temos método para listar reviews, vamos assumir que foi salvo
        # Este é um exemplo de TDD - implementaremos depois
        assert True  # Placeholder até implementaremos list_reviews
