from flask import jsonify, Blueprint, request
from src.data.helper import Helper

helper = Helper()
api = Blueprint('api', __name__)

@api.route('/product/<int:product_id>/', methods=['GET'])
def get_product(product_id):
    product = helper.get_product(product_id)
    response = {"product": product}
    return jsonify(response), 200

@api.route('/products', methods=['GET'])
def get_products():
    data = request.get_json()
    product_ids = data.get('products')
    products = helper.get_products_from_list(product_ids)
    response = {"product": products}
    return jsonify(response), 200