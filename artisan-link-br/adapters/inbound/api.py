from flask import Flask, jsonify, request
from core.entities import Product
from core.services import ProductService
from adapters.outbound.repository import ProductRepository


def create_app():
    app = Flask(__name__)

    product_repo = ProductRepository()
    product_service = ProductService(product_repo)

    @app.route("/products", methods=["GET"])
    def list_products():
        products = product_service.list_products()
        return jsonify([product.__dict__ for product in products])

    @app.route("/products", methods=["POST"])
    def add_product():
        data = request.json
        try:
            product = Product(
                id=data["id"],
                artisan_id=data["artisan_id"],
                name=data["name"],
                description=data["description"],
                price=data["price"],
            )
            product_service.add_product(product)
            return jsonify({"message": "Product added successfully"}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
