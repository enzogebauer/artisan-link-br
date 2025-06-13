import pytest
from core.entities import Product, Order, Review
from adapters.outbound.repository import ProductRepository, OrderRepository, ReviewRepository

class TestProductRepository:
    def test_save_product(self, product_repository):
        """Test saving a product to repository"""
        product = Product(
            id=1, 
            artisan_id=1, 
            name="Vaso de Cerâmica", 
            description="Vaso artesanal", 
            price=50.0
        )
        
        product_repository.save(product)
        products = product_repository.list_all()
        
        assert len(products) == 1
        assert products[0] == product
    
    def test_list_all_empty(self, product_repository):
        """Test listing all products when repository is empty"""
        products = product_repository.list_all()
        assert products == []
    
    def test_save_multiple_products(self, product_repository):
        """Test saving multiple products"""
        product1 = Product(id=1, artisan_id=1, name="Vaso", description="Vaso", price=50.0)
        product2 = Product(id=2, artisan_id=1, name="Prato", description="Prato", price=30.0)
        
        product_repository.save(product1)
        product_repository.save(product2)
        
        products = product_repository.list_all()
        assert len(products) == 2
        assert product1 in products
        assert product2 in products

class TestOrderRepository:
    def test_save_order(self, order_repository):
        """Test saving an order to repository"""
        products = [
            Product(id=1, artisan_id=1, name="Vaso", description="Vaso", price=50.0)
        ]
        order = Order(id=1, customer_id=1, products=products, total=50.0)
        
        order_repository.save(order)
        # Vamos implementar list_all para orders depois - TDD approach
        assert True  # Placeholder

class TestReviewRepository:
    def test_save_review(self, review_repository):
        """Test saving a review to repository"""
        review = Review(
            id=1, 
            product_id=1, 
            customer_id=1, 
            rating=5, 
            comment="Excelente!"
        )
        
        review_repository.save(review)
        # Vamos implementar list_all para reviews depois - TDD approach
        assert True  # Placeholder
