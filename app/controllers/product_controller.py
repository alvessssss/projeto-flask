from flask import request, jsonify
from app.models.product import Product
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_product():
    user = get_jwt_identity()

    if user['role'] != 'admin':
        return {"msg": "Apenas admin pode criar"}, 403

    data = request.json

    product = Product(
        name=data['name'],
        price=data['price'],
        user_id=user['id']
    )

    db.session.add(product)
    db.session.commit()

    return {"msg": "Produto criado"}


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
    user = get_jwt_identity()
    product = Product.query.get_or_404(id)

    if user['role'] != 'admin' and product.user_id != user['id']:
        return {"msg": "Sem permissão"}, 403

    data = request.json

    product.name = data['name']
    product.price = data['price']

    db.session.commit()

    return {"msg": "Atualizado"}


@jwt_required()
def delete_product(id):
    user = get_jwt_identity()
    product = Product.query.get_or_404(id)

    if user['role'] != 'admin':
        return {"msg": "Apenas admin pode deletar"}, 403

    db.session.delete(product)
    db.session.commit()

    return {"msg": "Deletado"}
