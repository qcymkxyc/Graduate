#!/usr/bin/python3
# coding=utf-8

"""
    配置文件
"""
from flask_uploads import UploadSet,IMAGES,AUDIO,configure_uploads,ALL,patch_request_class
import os

username = "root"
pw = "123456"
host = "47.94.80.98"
database = "graduate"

class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = "Flasky Admin <flasky@example.com>"
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True


    UPLOADED_DEFAULT_DEST = os.getcwd()
    UPLOADED_IMAGE_DEST = os.path.join(UPLOADED_DEFAULT_DEST,"data")
    UPLOADED_VIDEO_DEST = os.path.join(UPLOADED_DEFAULT_DEST,"data")

#   腾讯云COS
    COS_APPID = 1253764997
    COS_SECRET_ID = "AKIDZCJE4PylpmaQSKGTq11pS2TiojU3hddQ"
    COS_SECRET_KEY = "lKeTDqJahhiBwd7PUxePG3gImMII7we8"
    COS_REGION = "ap-chengdu"
    COS_BUCKET = "graduate-1253764997"
    COS_BUCKET_PATH = "https://{bucket}.cos.{region}.myqcloud.com".format(bucket=COS_BUCKET,region=COS_REGION)  #生成的Bucket基路径

    @staticmethod
    def init_app(app):
        pass

class DevelopementConfig(Config):

    DEBUG = True
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(username, pw, host, database)
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@47.94.80.98/graduate"


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(username, pw, host, database)



class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{0}:{1}@{2}/{3}".format(username, pw, host, database)



config = {
    "development": DevelopementConfig,
    "testing": TestingConfig,
    "production": ProductConfig,

    "default": DevelopementConfig
}

