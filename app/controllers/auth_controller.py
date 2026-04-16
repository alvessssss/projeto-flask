from flask import request, jsonify
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db

def register():
    data = request.json

    hashed_password = generate_password_hash(data['password'])
    role = data.get("role", "user")

    user = User(
        username=data['username'],
        password=hashed_password,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Usuário criado"}), 201


def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"msg": "Credenciais inválidas"}), 401

    token = create_access_token(identity={
        "id": user.id,
        "role": user.role
    })

    return jsonify(access_token=token)
