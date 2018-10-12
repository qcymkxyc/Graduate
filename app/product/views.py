from . import product_blueprint
from flask import render_template,request
from flask_login import current_user,login_required
from ..models import Product
from .forms import ProductAddForm,ProductFindForm
from .. import db,products_images,products_video
from app.util.product import save_product_local

@product_blueprint.route("/new_product",methods = ["GET","POST"])
def add_product():
    form = ProductAddForm()
    if form.validate_on_submit():
        Product.upload_product(form)
        return render_template("products/add_products.html", form=form)
    return render_template("products/add_products.html",form = form)

@product_blueprint.route("/list_products",methods = ["GET"])
def list_product():
    return render_template("products/list_products.html",)

@product_blueprint.route("/find_products",methods = ["GET","POST"])
def find_products():
    page = request.args.get(key="page",default=1,type=int)
    limit= request.args.get(key="limit",default=12,type=int)
    search_name = request.args.get(key="name",default="")

    filters = dict()
    filters["language_id"] = request.args.get(key="product_language",type=int,default=-1)

    paginate = (Product.query.filter(
                    Product.name.like("%" + search_name + "%"),
                    ).
                    filter(*filters).
                    order_by("id").
                    paginate(page = page,per_page=limit))

    items = paginate.items

    return render_template("products_list.html",items = items,pagination= paginate)

@product_blueprint.route("/custom",methods = ["GET"])
def custom():
    return render_template("custom.html")

@product_blueprint.route("/single_product",methods =["GET"])
def single_product():
    product_id = request.args.get("id",type=int)
    product = Product.query.filter_by(id=product_id).first()

    return render_template("single_product.html",product=product)

# @product_blueprint.route("/add_product1",methods = ["GET","POST"])
# def add_product1():

