import pytest
from core.entities import Artisan, Product, Order, Review


class TestArtisan:
    def test_artisan_creation(self):
        """Test that an Artisan can be created with valid data"""
        artisan = Artisan(id=1, name="João Silva", email="joao@email.com")

        assert artisan.id == 1
        assert artisan.name == "João Silva"
        assert artisan.email == "joao@email.com"

    def test_artisan_equality(self):
        """Test that two artisans with same data are equal"""
        artisan1 = Artisan(id=1, name="João Silva", email="joao@email.com")
        artisan2 = Artisan(id=1, name="João Silva", email="joao@email.com")

        assert artisan1 == artisan2


class TestProduct:
    def test_product_creation(self):
        """Test that a Product can be created with valid data"""
        product = Product(
            id=1,
            artisan_id=1,
            name="Vaso de Cerâmica",
            description="Vaso artesanal feito à mão",
            price=50.0,
        )

        assert product.id == 1
        assert product.artisan_id == 1
        assert product.name == "Vaso de Cerâmica"
        assert product.description == "Vaso artesanal feito à mão"
        assert product.price == 50.0

    def test_product_price_positive(self):
        """Test that product price should be positive"""
        with pytest.raises(ValueError):
            Product(id=1, artisan_id=1, name="Test", description="Test", price=-10.0)


class TestOrder:
    def test_order_creation(self):
        """Test that an Order can be created with valid data"""
        products = [
            Product(id=1, artisan_id=1, name="Vaso", description="Vaso", price=50.0),
            Product(id=2, artisan_id=1, name="Prato", description="Prato", price=30.0),
        ]
        order = Order(id=1, customer_id=1, products=products, total=80.0)

        assert order.id == 1
        assert order.customer_id == 1
        assert len(order.products) == 2
        assert order.total == 80.0


class TestReview:
    def test_review_creation(self):
        """Test that a Review can be created with valid data"""
        review = Review(
            id=1, product_id=1, customer_id=1, rating=5, comment="Produto excelente!"
        )

        assert review.id == 1
        assert review.product_id == 1
        assert review.customer_id == 1
        assert review.rating == 5
        assert review.comment == "Produto excelente!"

    def test_review_rating_range(self):
        """Test that review rating should be between 1 and 5"""
        with pytest.raises(ValueError):
            Review(id=1, product_id=1, customer_id=1, rating=6, comment="Test")
