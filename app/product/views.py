from . import product_blueprint
from flask import render_template,redirect
from flask_login import current_user,login_required
from ..models import Product
from .forms import ProductAddForm,ProductFindForm
from .. import db,products_images,products_video
from ..util.product import save_product

@product_blueprint.route("/new_product",methods = ["GET","POST"])
def add_product():
    form = ProductAddForm()
    if form.validate_on_submit():
        product = Product()
        product.name = form.name.data
        product.description = form.description.data
        product.language_id = form.language.data
        product.is_doc = form.have_doc.data
        product.baidu_url = form.baidu_url.data
        product.prices = form.price.data

        save_product(form,product)

        db.session.add(product)
        db.session.commit()
        # print(product.id)
        # return render_template(url_for("main"))
        return render_template("products/add_products.html", form=form)
    return render_template("products/add_products.html",form = form)

@product_blueprint.route("/list_products",methods = ["GET"])
def list_product():
    return render_template("products/list_products.html",)

@product_blueprint.route("/find_products",methods = ["GET"])
def find_product():
    form = ProductFindForm()
    return render_template("products/find_products.html",form = form)