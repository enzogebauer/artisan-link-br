import pytest
import json
from adapters.inbound.api import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


AUTH_TOKEN = "Bearer meu-token-secreto"


class TestOrderAPI:
    def test_create_order(self, client):
        """Test creating a new order"""
        order_data = {
            "customer_id": 1,
            "products": [{"id": 1, "quantity": 2}],
            "total": 100.0,
        }
        response = client.post(
            "/orders",
            data=json.dumps(order_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["customer_id"] == 1
        assert data["total"] == 100.0

    def test_create_order_missing_data(self, client):
        """Test creating an order with missing data"""
        order_data = {"customer_id": 1}
        response = client.post(
            "/orders",
            data=json.dumps(order_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_get_order(self, client):
        """Test getting an order by ID"""
        # First create an order
        order_data = {
            "customer_id": 1,
            "products": [{"id": 1, "quantity": 2}],
            "total": 100.0,
        }
        response = client.post(
            "/orders",
            data=json.dumps(order_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        order_id = data["id"]

        # Then get the order
        response = client.get(
            f"/orders/{order_id}", headers={"Authorization": AUTH_TOKEN}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["customer_id"] == 1
        assert data["total"] == 100.0

    def test_update_order(self, client):
        """Test updating an existing order"""
        # First create an order
        order_data = {
            "customer_id": 1,
            "products": [{"id": 1, "quantity": 2}],
            "total": 100.0,
        }
        response = client.post(
            "/orders",
            data=json.dumps(order_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        order_id = data["id"]

        # Then update the order
        update_data = {"total": 120.0}
        response = client.put(
            f"/orders/{order_id}",
            data=json.dumps(update_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["total"] == 120.0

    def test_delete_order(self, client):
        """Test deleting an existing order"""
        # First create an order
        order_data = {
            "customer_id": 1,
            "products": [{"id": 1, "quantity": 2}],
            "total": 100.0,
        }
        response = client.post(
            "/orders",
            data=json.dumps(order_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        order_id = data["id"]

        # Then delete the order
        response = client.delete(
            f"/orders/{order_id}", headers={"Authorization": AUTH_TOKEN}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "message" in data


class TestReviewAPI:
    def test_create_review(self, client):
        """Test creating a new review"""
        review_data = {
            "product_id": 1,
            "customer_id": 1,
            "rating": 5,
            "comment": "Great product!",
        }
        response = client.post(
            "/reviews",
            data=json.dumps(review_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["product_id"] == 1
        assert data["rating"] == 5

    def test_create_review_missing_data(self, client):
        """Test creating a review with missing data"""
        review_data = {"product_id": 1, "customer_id": 1}
        response = client.post(
            "/reviews",
            data=json.dumps(review_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_update_review(self, client):
        """Test updating an existing review"""
        # First create a review
        review_data = {
            "product_id": 1,
            "customer_id": 1,
            "rating": 5,
            "comment": "Great product!",
        }
        response = client.post(
            "/reviews",
            data=json.dumps(review_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        review_id = data["id"]

        # Then update the review
        update_data = {"rating": 4, "comment": "Good product!"}
        response = client.put(
            f"/reviews/{review_id}",
            data=json.dumps(update_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["rating"] == 4
        assert data["comment"] == "Good product!"

    def test_delete_review(self, client):
        """Test deleting an existing review"""
        # First create a review
        review_data = {
            "product_id": 1,
            "customer_id": 1,
            "rating": 5,
            "comment": "Great product!",
        }
        response = client.post(
            "/reviews",
            data=json.dumps(review_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        review_id = data["id"]

        # Then delete the review
        response = client.delete(
            f"/reviews/{review_id}", headers={"Authorization": AUTH_TOKEN}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "message" in data
