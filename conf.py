#!/usr/bin/python3
# coding=utf-8

"""
    配置文件
"""
import os
import logging
import logging.config

username = "root"
pw = "123456"
host = "47.94.80.98"
database = "graduate"


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"

    MAIL_SUBJECT_PREFIX = '[易帮计算机毕业设计]'
    MAIL_SENDER = "yibangbishe@163.com"
    ADMIN = "qcymkxyc@163.com"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True

    UPLOADED_DEFAULT_DEST = os.getcwd()
    UPLOADED_IMAGE_DEST = os.path.join(UPLOADED_DEFAULT_DEST, "data")
    UPLOADED_VIDEO_DEST = os.path.join(UPLOADED_DEFAULT_DEST, "data")

#   腾讯云COS
    COS_APPID = 1253764997
    COS_SECRET_ID = "AKIDZCJE4PylpmaQSKGTq11pS2TiojU3hddQ"
    COS_SECRET_KEY = "lKeTDqJahhiBwd7PUxePG3gImMII7we8"
    COS_REGION = "ap-chengdu"
    COS_BUCKET = "graduate-1253764997"
    # 生成的Bucket基路径
    COS_BUCKET_PATH = "https://{bucket}.cos.{region}.myqcloud.com".format(bucket=COS_BUCKET, region=COS_REGION)

    @staticmethod
    def init_app(app):
        pass


class DevelopementConfig(Config):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(username, pw, host, database)


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(username, pw, host, database)


class ProductConfig(Config):

    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 25
    MAIL_USE_SSL = True
    MAIL_USERNAME = "yibangbishe@163.com"
    MAIL_PASSWORD = "68415843gG"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(username, pw, host, database)

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        from logging.handlers import SMTPHandler
        # 日志
        logging.config.fileConfig(fname="logger.conf", defaults=None, disable_existing_loggers=True)
        app.logger = logging.getLogger("root")
        if getattr(cls, "MAIL_USERNAME", None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, "MAIL_USE_SSL", None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + " Application Error",
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(mail_handler)


config = {
    "development": DevelopementConfig,
    "testing": TestingConfig,
    "production": ProductConfig,

    "default": DevelopementConfig
}
