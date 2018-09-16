#!/usr/bin/python3
# coding=utf-8

import hashlib
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from . import login_manager,db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request
from datetime import datetime

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
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["FLASKY_ADMIN"]:
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

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),index = True)
    language_id = db.Column(db.Integer,db.ForeignKey("t_language.id"))

    #产品描述
    description = db.Column(db.String(1024))

    #图片路径
    picture1_path = db.Column(db.String(256))
    picture2_path = db.Column(db.String(256))
    picture3_path = db.Column(db.String(256))

    #视频
    video_path = db.Column(db.String(256))
    #是否有毕业论文
    is_doc = db.Column(db.Boolean,default = False)


class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser
