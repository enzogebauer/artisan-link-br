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


class TestArtisanAPI:
    def test_create_artisan(self, client):
        """Test creating a new artisan"""
        artisan_data = {"name": "João Silva", "email": "joao@email.com"}
        response = client.post(
            "/artisans",
            data=json.dumps(artisan_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["name"] == "João Silva"
        assert data["email"] == "joao@email.com"

    def test_create_artisan_missing_data(self, client):
        """Test creating an artisan with missing data"""
        artisan_data = {"name": "João Silva"}
        response = client.post(
            "/artisans",
            data=json.dumps(artisan_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_create_artisan_unauthorized(self, client):
        """Test creating an artisan without authorization"""
        artisan_data = {"name": "João Silva", "email": "joao@email.com"}
        response = client.post(
            "/artisans", data=json.dumps(artisan_data), content_type="application/json"
        )
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data

    def test_update_artisan(self, client):
        """Test updating an existing artisan"""
        # First create an artisan
        artisan_data = {"name": "João Silva", "email": "joao@email.com"}
        response = client.post(
            "/artisans",
            data=json.dumps(artisan_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        artisan_id = data["id"]

        # Then update the artisan
        update_data = {"name": "Maria Silva", "email": "maria@email.com"}
        response = client.put(
            f"/artisans/{artisan_id}",
            data=json.dumps(update_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["name"] == "Maria Silva"
        assert data["email"] == "maria@email.com"

    def test_delete_artisan(self, client):
        """Test deleting an existing artisan"""
        # First create an artisan
        artisan_data = {"name": "João Silva", "email": "joao@email.com"}
        response = client.post(
            "/artisans",
            data=json.dumps(artisan_data),
            content_type="application/json",
            headers={"Authorization": AUTH_TOKEN},
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        artisan_id = data["id"]

        # Then delete the artisan
        response = client.delete(
            f"/artisans/{artisan_id}", headers={"Authorization": AUTH_TOKEN}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "message" in data
