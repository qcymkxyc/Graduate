from . import product_blueprint
from flask import render_template,redirect,url_for,flash
from flask_login import current_user,login_required

@product_blueprint.route("/add_product",methods = ["GET","POST"])
def add_product():
    pass