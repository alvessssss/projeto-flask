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
    data = request.get_json()

    if not data:
        return jsonify({"msg": "JSON inválido"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Campos obrigatórios faltando"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"msg": "Usuário não encontrado"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"msg": "Senha incorreta"}), 401

    token = create_access_token(
        identity=str(user.id),
    additional_claims={"role": user.role}
    )

    return jsonify(access_token=token), 200





