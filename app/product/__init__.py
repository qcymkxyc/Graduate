from flask import blueprints

product_blueprint = blueprints.Blueprint("products",__name__)

from . import views,forms