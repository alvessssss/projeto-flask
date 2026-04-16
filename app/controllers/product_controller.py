from flask import request, jsonify
from app.models.product import Product
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


# 🔹 CRIAR PRODUTO
@jwt_required()
def create_product():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get("role")

    # 🔐 Apenas admin pode criar
    if role != 'administrador':
        return {"msg": "Apenas admin pode criar"}, 403

    data = request.get_json()

    # 🔥 Validação do JSON
    if not data:
        return {"msg": "JSON inválido ou vazio"}, 400

    if 'name' not in data or 'price' not in data:
        return {"msg": "Campos obrigatórios: name, price"}, 400

    product = Product(
        name=data['name'],
        price=data['price'],
        user_id=user_id
    )

    db.session.add(product)
    db.session.commit()

    return {"msg": "Produto criado"}, 201


# 🔹 LISTAR PRODUTOS
@jwt_required()
def list_products():
    products = Product.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "user_id": p.user_id
        } for p in products
    ])


# 🔹 ATUALIZAR PRODUTO
@jwt_required()
def update_product(id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get("role")

    product = Product.query.get_or_404(id)

    # 🔐 Admin ou dono pode editar
    if role != 'administrador' and product.user_id != user_id:
        return {"msg": "Sem permissão"}, 403

    data = request.get_json()

    if not data:
        return {"msg": "JSON inválido ou vazio"}, 400

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)

    db.session.commit()

    return {"msg": "Atualizado"}, 200


# 🔹 DELETAR PRODUTO
@jwt_required()
def delete_product(id):
    claims = get_jwt()
    role = claims.get("role")

    product = Product.query.get_or_404(id)

    # 🔐 Apenas admin pode deletar
    if role != 'administrador':
        return {"msg": "Apenas admin pode deletar"}, 403

    db.session.delete(product)
    db.session.commit()

    return {"msg": "Deletado"}, 200