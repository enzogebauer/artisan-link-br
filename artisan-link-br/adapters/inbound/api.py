from flask import Flask, jsonify, request
from core.entities import Product, Artisan, Order, Review
from core.services import ProductService
from adapters.outbound.repository import ProductRepository


# Função de autenticação simples
def require_auth():
    auth = request.headers.get("Authorization")
    if auth != "Bearer meu-token-secreto":
        return jsonify({"error": "Não autorizado."}), 401


def create_app():
    app = Flask(__name__)

    # Repositórios e serviços
    product_repo = ProductRepository()
    product_service = ProductService(product_repo)

    # Repositórios simples em memória para artesãos, orders e reviews
    artisans = {}
    orders = {}
    reviews = {}

    # --- Produtos ---
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

    # --- Artesãos ---
    @app.route("/artisans", methods=["POST"])
    def create_artisan():
        auth_error = require_auth()
        if auth_error:
            return auth_error

        data = request.json
        if not data.get("name") or not data.get("email"):
            return jsonify({"error": "Nome e email são obrigatórios."}), 400
        if any(a.email == data["email"] for a in artisans.values()):
            return jsonify({"error": "Email já cadastrado."}), 400

        try:
            artisan = Artisan(
                id=len(artisans) + 1, name=data["name"], email=data["email"]
            )
            artisans[artisan.id] = artisan
            return (
                jsonify(
                    {"id": artisan.id, "name": artisan.name, "email": artisan.email}
                ),
                201,
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/artisans/<int:artisan_id>", methods=["PUT"])
    def update_artisan(artisan_id):
        auth_error = require_auth()
        if auth_error:
            return auth_error

        data = request.json
        artisan = artisans.get(artisan_id)
        if not artisan:
            return jsonify({"error": "Artesão não encontrado."}), 404

        if "email" in data:
            if any(
                a.email == data["email"] and a.id != artisan_id
                for a in artisans.values()
            ):
                return jsonify({"error": "Email já cadastrado."}), 400
            artisan.email = data["email"]

        if "name" in data:
            artisan.name = data["name"]

        return jsonify({"id": artisan.id, "name": artisan.name, "email": artisan.email})

    @app.route("/artisans/<int:artisan_id>", methods=["DELETE"])
    def delete_artisan(artisan_id):
        auth_error = require_auth()
        if auth_error:
            return auth_error

        if artisan_id not in artisans:
            return jsonify({"error": "Artesão não encontrado."}), 404
        del artisans[artisan_id]
        return jsonify({"message": "Artesão removido com sucesso."})

    @app.route("/artisans", methods=["GET"])
    def list_artisans():
        return jsonify(
            [{"id": a.id, "name": a.name, "email": a.email} for a in artisans.values()]
        )

    # --- Pedidos (Orders) ---
    @app.route("/orders", methods=["POST"])
    def create_order():
        auth_error = require_auth()
        if auth_error:
            return auth_error

        data = request.json
        if (
            not data.get("customer_id")
            or not data.get("products")
            or not data.get("total")
        ):
            return (
                jsonify({"error": "customer_id, products e total são obrigatórios."}),
                400,
            )

        try:
            products_list = []
            for p in data["products"]:
                product_obj = Product(
                    id=p.get("id"),
                    artisan_id=p.get("artisan_id", 0),
                    name=p.get("name", ""),
                    description=p.get("description", ""),
                    price=p.get("price", 0.0),
                )
                products_list.append(product_obj)

            order = Order(
                id=len(orders) + 1,
                customer_id=data["customer_id"],
                products=products_list,
                total=data["total"],
            )
            orders[order.id] = order
            return (
                jsonify(
                    {
                        "id": order.id,
                        "customer_id": order.customer_id,
                        "total": order.total,
                    }
                ),
                201,
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/orders/<int:order_id>", methods=["PUT"])
    def update_order(order_id):
        auth_error = require_auth()
        if auth_error:
            return auth_error

        order = orders.get(order_id)
        if not order:
            return jsonify({"error": "Pedido não encontrado."}), 404

        data = request.json
        if "customer_id" in data:
            order.customer_id = data["customer_id"]
        if "products" in data:
            products_list = []
            for p in data["products"]:
                product_obj = Product(
                    id=p.get("id"),
                    artisan_id=p.get("artisan_id", 0),
                    name=p.get("name", ""),
                    description=p.get("description", ""),
                    price=p.get("price", 0.0),
                )
                products_list.append(product_obj)
            order.products = products_list
        if "total" in data:
            order.total = data["total"]

        return jsonify(
            {"id": order.id, "customer_id": order.customer_id, "total": order.total}
        )

    @app.route("/orders/<int:order_id>", methods=["DELETE"])
    def delete_order(order_id):
        auth_error = require_auth()
        if auth_error:
            return auth_error

        if order_id not in orders:
            return jsonify({"error": "Pedido não encontrado."}), 404
        del orders[order_id]
        return jsonify({"message": "Pedido removido com sucesso."})

    @app.route("/orders/<int:order_id>", methods=["GET"])
    def get_order(order_id):
        auth_error = require_auth()
        if auth_error:
            return auth_error

        order = orders.get(order_id)
        if not order:
            return jsonify({"error": "Pedido não encontrado."}), 404

        # Converte os objetos Product de volta para dicionários para serializar em JSON
        products_data = []
        for product in order.products:
            products_data.append(product.__dict__)

        order_data = {
            "id": order.id,
            "customer_id": order.customer_id,
            "products": products_data,
            "total": order.total,
        }

        return jsonify(order_data), 200

    # --- Avaliações (Reviews) ---
    @app.route("/reviews", methods=["POST"])
    def create_review():
        auth_error = require_auth()
        if auth_error:
            return auth_error

        data = request.json
        required_fields = ["product_id", "customer_id", "rating", "comment"]
        if not all(field in data for field in required_fields):
            return (
                jsonify(
                    {
                        "error": "Todos os campos são obrigatórios: product_id, customer_id, rating, comment."
                    }
                ),
                400,
            )

        try:
            review = Review(
                id=len(reviews) + 1,
                product_id=data["product_id"],
                customer_id=data["customer_id"],
                rating=data["rating"],
                comment=data["comment"],
            )
            reviews[review.id] = review
            return (
                jsonify(
                    {
                        "id": review.id,
                        "product_id": review.product_id,
                        "rating": review.rating,
                    }
                ),
                201,
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/reviews/<int:review_id>", methods=["PUT"])
    def update_review(review_id):
        auth_error = require_auth()
        if auth_error:
            return auth_error

        review = reviews.get(review_id)
        if not review:
            return jsonify({"error": "Avaliação não encontrada."}), 404

        data = request.json
        if "rating" in data:
            review.rating = data["rating"]
        if "comment" in data:
            review.comment = data["comment"]

        return jsonify(
            {"id": review.id, "rating": review.rating, "comment": review.comment}
        )

    @app.route("/reviews/<int:review_id>", methods=["DELETE"])
    def delete_review(review_id):
        auth_error = require_auth()
        if auth_error:
            return auth_error

        if review_id not in reviews:
            return jsonify({"error": "Avaliação não encontrada."}), 404
        del reviews[review_id]
        return jsonify({"message": "Avaliação removida com sucesso."})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
