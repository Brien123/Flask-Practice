from http.client import responses

from flask import jsonify, Blueprint, request
from src.data.helper import Helper
from src.elasticsearch.elasticsearch_client import ElasticSearchClient
from src.elasticsearch.mapping import products_mapping

helper = Helper()
elasictsearch_client = ElasticSearchClient()
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

@api.route('/category/<int:category_id>/', methods=['GET'])
def get_products_by_category(category_id):
    products = helper.get_product_by_category(category_id=category_id)
    response = {"products": products}
    return jsonify(response), 200

@api.route('/user/<int:user_id>/', methods=['GET'])
def get_products_by_user(user_id):
    products = helper.get_product_by_user(user_id=user_id)
    response = {"products": products}
    return jsonify(response), 200

@api.route('/create-index', methods=['POST'])
def create_index():
    data = request.get_json()
    index_name = data.get('index_name')
    if index_name == "products":
        mapping = products_mapping
        status = elasictsearch_client.create_index(index_name=index_name, mapping=mapping)
        response = {"status": status}
        return jsonify(response), 200
    else:
        response = {"status": False}
        return jsonify(response), 200

@api.route('/delete-index', methods=['POST'])
def delete_index():
    data = request.get_json()
    index_name = data.get('index_name')
    if index_name == "products":
        status = elasictsearch_client.delete_index(index_name=index_name)
        response = {"status": status}
        return jsonify(response), 200
    else:
        response = {"status": False}
        return jsonify(response), 200

@api.route('/load-products-into-elasticsearch', methods=['POST'])
def load_products_into_search():
    products = helper.get_products()
    status = elasictsearch_client.bulk_index_products_data(products_data=products)
    response = {"status": status}
    return jsonify(response), 200

@api.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    search_term = data.get('search_term')
    index_name = data.get('index_name', 'products')
    size = data.get('size', 10)
    page = data.get('page', 1)
    results = elasictsearch_client.search(search_term=search_term, index_name=index_name, size=size, page=page)
    response = {"results": results}
    return jsonify(response), 200

@api.route("/web-products", methods=["GET"])
def web_products():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 20, type=int)
    products = helper.fetch_products(page=page, size=size)
    response = {"products": products}
    return jsonify(response), 200