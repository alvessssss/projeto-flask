from flask import request, jsonify
from app.models.product import Product
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


@jwt_required()
def create_product():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get("role")

    if role != 'administrador':
        return {"msg": "Apenas admin pode criar"}, 403

    data = request.get_json()

    product = Product(
        name=data['name'],
        price=data['price'],
        user_id=user_id
    )

    db.session.add(product)
    db.session.commit()

    return {"msg": "Produto criado"}, 201


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


@jwt_required()
def update_product(id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get("role")

    product = Product.query.get_or_404(id)

    if role != 'administrador' and product.user_id != user_id:
        return {"msg": "Sem permissão"}, 403

    data = request.get_json()

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)

    db.session.commit()

    return {"msg": "Atualizado"}


@jwt_required()
def delete_product(id):
    claims = get_jwt()
    role = claims.get("role")

    product = Product.query.get_or_404(id)

    if role != 'administrador':
        return {"msg": "Apenas admin pode deletar"}, 403

    db.session.delete(product)
    db.session.commit()

    return {"msg": "Deletado"}
