from flask import jsonify,request
from .. import db
from ..models import Product
from . import api

@api.route("/products")
def get_products():
    print(request.args)
    page = request.args.get("page")
    return jsonify({
        "data" : [p.to_json() for p in Product.query.all()],
        "count" : 10,
        "msg" : "ddddd",
        "code" : 0
    })