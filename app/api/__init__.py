from flask.blueprints import Blueprint

api = Blueprint("api",__name__)

from . import users,errors,products,authentication