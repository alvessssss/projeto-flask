from flask import Flask
from app.config import Config
from app import db
from flask_jwt_extended import JWTManager
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
jwt = JWTManager(app)

@app.route("/")
def home():
    return "API rodando "

app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
