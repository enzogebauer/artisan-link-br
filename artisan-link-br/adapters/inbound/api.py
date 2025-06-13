from flask import Flask, jsonify, request
from core.entities import Product, Artisan
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

    # Repositório simples em memória para artesãos
    artisans = {}

    # Endpoints de produtos (já existentes)
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

    # Endpoints de artesãos (novos)
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

        # Validação de email único (se fornecido)
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
        """Endpoint adicional para listar artesãos (útil para debug)"""
        return jsonify(
            [{"id": a.id, "name": a.name, "email": a.email} for a in artisans.values()]
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
