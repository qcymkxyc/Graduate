#!/usr/bin/python3
# coding=utf-8

import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime

from app.util import cos
from conf import Config


class User(db.Model,UserMixin):
    __tablename__ = "t_user"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20),unique = True,index = True)
    hash_password = db.Column(db.String(128))
    email = db.Column(db.String(64),unique = True,index = True)
    about_me = db.Column(db.Text())
    location = db.Column(db.String(64))
    last_seen = db.Column(db.DateTime(),default = datetime.utcnow)
    member_since = db.Column(db.DateTime(),default = datetime.utcnow)

    role_id = db.Column(db.Integer,db.ForeignKey("t_role.id"))

    confirmed = db.Column(db.Boolean,default = False)

    def __init__(self,**kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["ADMIN"]:
                self.role = Role.query.filter_by(permission = 0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default = True).first()

    @property
    def password(self):
        raise AttributeError("你没有权限直接查看密码")

    @password.setter
    def password(self,password):
        self.hash_password = generate_password_hash(password)

    def vertify_password(self,password):
        """
        验证密码是否同存储的密码一致
        :param password:
        :return:
        """
        return check_password_hash(self.hash_password,password)

    def generate_confirmation_token(self,expiration = 3600):
        s = Serializer(current_app.config["SECRET_KEY"],expiration)
        return s.dumps({"confirm" : self.id})

    def confirm(self,token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = "t_role"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique = True,index = True)
    default = db.Column(db.Boolean,default = False,index = True)
    permissions = db.Column(db.Integer)

    users = db.relationship("User",backref = "role")

    def insert_roles(self):
        roles = {
            "User" : (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            "Moderator" : (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS,False),
            "Administrator" : (0xff , False)
        }
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)

            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def can(self,permissions):
        return (self.role is not None and
                (self.role.permissions & permissions) == permissions)

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


class Language(db.Model):
    __tablename__ = "t_language"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique = True,index = True)
    products = db.relationship("Product",backref = "language")


class Product(db.Model):
    __tablename__ = "t_product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    language_id = db.Column(db.Integer, db.ForeignKey("t_language.id"), index=True)

    # 产品描述
    description = db.Column(db.String(1024))

    # 图片路径
    imgs_path = db.Column(db.String(1024), comment="图片路径")

    # 视频
    video_path = db.Column(db.String(256))

    # 是否有毕业论文
    is_doc = db.Column(db.Boolean, default=False, index=True, comment="是否有毕业论文")
    prices = db.Column(db.FLOAT, default=100.)
    baidu_url = db.Column(db.String(256), comment="百度云url")

    def to_json(self):
        json_product = {
            "id": self.id,
            "name": self.name,
            "language_id": self.language_id,
            "language": self.language.name,
            "description": self.description,
            "imgs_path": self.imgs_path.split(";"),
            "video_path": self.video_path,
            "is_doc": self.is_doc
        }
        return json_product

    @staticmethod
    def from_json(json_product):
        product = Product()
        product.id = json_product.get("id")
        product.name = json_product.get("name")
        product.language_id = json_product.get("language_id")
        product.description = json_product.get("description")
        product.video_path = json_product.get("video_path")
        product.is_doc = json_product.get("is_doc")
        product.imgs_path = ";".join(json_product.imgs_path)

        return product

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            p = Product(
                name=forgery_py.name.full_name(),
                language_id=randint(1, 6),
                description=forgery_py.lorem_ipsum.paragraph(sentences_quantity=10),
                video_path=forgery_py.lorem_ipsum.word(),
                baidu_url=forgery_py.internet.domain_name(),
                prices=randint(0, 2000),
                is_doc=False
            )
            # 生成图片路径
            imgs_path = ""
            for i in range(10):
                imgs_path += forgery_py.lorem_ipsum.sentence() + ";"
            p.imgs_path = imgs_path

            db.session.add(p)

            try:
                db.session.commit()
            except:
                db.session.rollback()

    @staticmethod
    def upload_product(product_form):
        """上传文件

        分两次提交数据库，第一次提交拿到数据的id，用id生成保存的文件夹名，再将
        文件上传至COS该文件夹下，第二次将COS上对应的文件路径存进数据库

        :param product_form:Form
            产品上传数据
        """
        product = Product()
        product.name = product_form.name.data
        product.description = product_form.description.data
        product.language_id = product_form.language.data
        product.is_doc = product_form.have_doc.data
        product.baidu_url = product_form.baidu_url.data
        product.prices = product_form.price.data

        db.session.add(product)
        try:
            db.session.commit()

            # 视频地址
            video_path = "{id}/video.mp4".format(id=product.id)

            # 图片地址
            imgs_path = []
            for img in product_form.imgs.data:
                img_path = "{id}/{name}".format(id=product.id, name=img.filename)
                imgs_path.append(img_path)

            # 上传文件
            cos.upload_binary_file(binary_file=product_form.video.data,key=video_path)
            for i, img_path in enumerate(imgs_path):
                img = product_form.imgs.data[i]
                cos.upload_binary_file(binary_file=img, key=img_path)

            # 数据库保存地址
            product.video_path = Config.COS_BUCKET_PATH + "/" + video_path  # 视频地址
            save_imgs_path = map(lambda x: Config.COS_BUCKET_PATH + "/" + x, imgs_path)     # 图片地址
            product.imgs_path = ";".join(save_imgs_path)

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()


class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.anonymous_user = AnonymousUser
