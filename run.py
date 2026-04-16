from flask import Flask
from app.config import Config
from app import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp


app = Flask(__name__)
app.config.from_object(Config)


# Inicializações
db.init_app(app)
jwt = JWTManager(app)


# Rota básica
@app.route("/")
def home():
    return "API rodando"


# 🔐 ROTA PROTEGIDA
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user = get_jwt_identity()
    return {
        "msg": "Acesso permitido",
        "user": user
    }, 200


# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)


# Criar tabelas
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)





