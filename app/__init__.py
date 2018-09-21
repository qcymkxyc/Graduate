#!/usr/bin/python3
# coding=utf-8

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager

import conf
from flask_uploads import UploadSet,configure_uploads,IMAGES,AUDIO

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy(use_native_unicode="utf8")
moment = Moment()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

products_images = UploadSet("image",IMAGES,)
products_video = UploadSet("video",("flv","mp4"))

def create_app(config_name = "default"):
    """
    工厂类，创建应用
    :param config_name: 配置名
    :return: 应用
    """

    app = Flask(__name__)
    app.config.from_object(conf.config[config_name])
    conf.config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    configure_uploads(app,products_images)
    configure_uploads(app,products_video)

    from .main import main
    app.register_blueprint(main)
    from .auth import auth
    app.register_blueprint(auth,url_prefix = "/auth")
    from .product import product_blueprint
    app.register_blueprint(product_blueprint,url_prefix = "/products")
    from .api import api
    app.register_blueprint(api,url_prefix = "/api/v1")

    return app;

