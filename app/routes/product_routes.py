from flask import Blueprint
from app.controllers import product_controller

product_bp = Blueprint('product', __name__)

product_bp.route('/products', methods=['GET'])(product_controller.list_products)
product_bp.route('/products', methods=['POST'])(product_controller.create_product)
product_bp.route('/products/<int:id>', methods=['PUT'])(product_controller.update_product)
product_bp.route('/products/<int:id>', methods=['DELETE'])(product_controller.delete_product)
