from flask import Blueprint, request, render_template

from src.data.helper import Helper

web = Blueprint("web", __name__)
helper = Helper()

@web.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 20, type=int)
    products = helper.fetch_products(page=page, size=size)
    for i in products:
        i["image_medium"] = "https://buyam.co/storage/products/" + i.get("image_medium") if i.get(
            "image_thumb") else None

    return render_template("web/home.html", products=products, page=page, size=size)




@web.route("/product/<int:product_id>")
def product(product_id):
  page = request.args.get("page", 1, type=int)
  size = request.args.get("size",5, type=int)
  product = helper.get_product(product_id)
  product["image_medium"] = "https://buyam.co/storage/products/" + product.get("image_medium") if product.get(
 "image_thumb") else None
  product_list = helper.get_product_by_user( product.get('user_id'), page=page, size=size)
  for i in product_list: 
    
    i["image_medium"] = "https://buyam.co/storage/products/" + i.get("image_medium") if i.get(
    "image_thumb") else None



  return render_template("web/product.html", product=product, product_list=product_list, size=size, page=page) 


"""@web.route("/product/<int:product_id>")
def product(product_id):
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 5, type=int)
    
    product = helper.get_product(product_id)
    
    if not product:None

    product["image_medium"] = "https://buyam.co/storage/products/" + product.get("image_medium") if product.get("image_thumb") else None
    
    category_id_for_list = product.get('category_id')
    product_list = helper.get_product_by_category(category_id_for_list, page=page, size=size)
    
    for i in product_list:
        i["image_medium"] = "https://buyam.co/storage/products/" + i.get("image_medium") if i.get("image_thumb") else None

    return render_template("web/category.html", product=product, product_list=product_list, size=size, page=page)"""

