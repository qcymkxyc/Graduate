from flask import jsonify, request, current_app
from ..models import Product
from . import api
from app.product.forms import ProductAddForm


@api.route("/products")
def get_products():
    page = request.args.get(key="page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    paginate = Product.query.order_by("id").paginate(page=page, per_page=limit)

    items = paginate.items
    total_page = paginate.pages
    return jsonify({
        "data": [p.to_json() for p in items],
        "count": total_page * limit,
        "msg": "",
        "code": 0
    })


@api.route("new_product", methods=["POST", "GET"])
def new_product():
    form = ProductAddForm()
    try:
        Product.upload_product(form)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({
            "msg": "error",
            "reason" : str(e)
        })
    else:
        return jsonify({"msg": "success"})


@api.route("find_product")
def find_product():
    page = request.args.get(key="page", default=1, type=int)
    limit = request.args.get(key="limit", type=int)
    search_name = request.args.get(key="search_name")

    filters = dict()
    filters["language_id"] = request.args.get(key="product_language", type=int)
    # TODO 不考虑以下情况
    # filters["have_doc"] = request.args.get(key="have_doc",type=int)
    # filters["have_img"] = request.args.get(key="have_img",type=int)
    # filters["have_video"] = request.args.get(key="have_video",type=int)

    conditions = []
    for key in filters.keys():
        value = filters[key]
        if value == -1:
            conditions.append(key)
        elif key != "language_id":
            filters[key] = bool(value)

    for k in conditions:
        filters.pop(k)

    paginate = (Product.query.filter(
        Product.name.like("%" + search_name + "%"),
        ).
        filter(*filters).
        order_by("id").
        paginate(page=page, per_page=limit))

    items = paginate.items
    total_page = paginate.pages
    return jsonify({
        "data": [p.to_json() for p in items],
        "count": total_page * limit,
        "msg": "",
        "code": 0
    })
