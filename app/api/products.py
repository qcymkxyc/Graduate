from flask import jsonify,request
from .. import db
from ..models import Product
from . import api

@api.route("/products")
def get_products():
    page = request.args.get(key = "page",default = 1,type = int)
    limit = request.args.get("limit",default = 10,type = int)
    paginate = Product.query.order_by("id").paginate(page=page, per_page=limit)

    items = paginate.items
    total_page = paginate.pages
    current_page = paginate.page
    return jsonify({
        "data" : [p.to_json() for p in items],
        "count" : total_page * limit,
        "msg" : "",
        "code" : 0
    })

@api.route("new_products")
def new_product():
    pass

@api.route("find_product")
def find_product():
    pass