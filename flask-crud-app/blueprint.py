
from flask import Blueprint
from controller import welcome, add_product, update_product, update_price, add_store, get_products_store

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(welcome)
blueprint.route('/product', methods=['POST'])(add_product)
blueprint.route('/product/<int:id>', methods=['PUT'])(update_product)
blueprint.route('/product/<int:id>/price', methods=['PUT'])(update_price)
blueprint.route('/store', methods=['POST'])(add_store)
blueprint.route('/store/<int:id>/products', methods=['GET'])(get_products_store)