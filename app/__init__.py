#!/usr/bin/python3
# coding=utf-8

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from qcloud_cos import CosConfig, CosS3Client

import conf

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy(use_native_unicode="utf8")
moment = Moment()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

# 文件上传组件
products_images = UploadSet("image", IMAGES,)
products_video = UploadSet("video", ("flv", "mp4"))

# 腾讯云COS配置和客户端
cos_config = CosConfig(
    Region=conf.Config.COS_REGION,
    Secret_id=conf.Config.COS_SECRET_ID,
    Secret_key=conf.Config.COS_SECRET_KEY)
cos_client = CosS3Client(cos_config)


def create_app(config_name):
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

    # flask-upload
    configure_uploads(app, products_images)
    configure_uploads(app, products_video)

    # jinja2
    from app.product import filter
    jinja_env = app.jinja_env
    jinja_env.filters["picc"] = filter.cos_picc_filter  # 数据万象的过滤器

    # 蓝图配置
    from .main import main
    app.register_blueprint(main)
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")
    from .product import product_blueprint
    app.register_blueprint(product_blueprint, url_prefix="/products")
    from .api import api
    app.register_blueprint(api, url_prefix="/api/v1")

    return app
