#!/usr/bin/python3
# coding=utf-8

from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager,db

class User(db.Model,UserMixin):
    __tablename__ = "t_user"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20),unique = True,index = True)
    hash_password = db.Column(db.String(128))
    email = db.Column(db.String(64),unique = True,index = True)

    role_id = db.Column(db.Integer,db.ForeignKey("t_role.id"))

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



class Role(db.Model):
    __tablename__ = "t_role"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique = True,index = True)
    users = db.relationship("User",backref = "role")


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

@login_manager.user_loader
def load_user(user_id):
    if __name__ == '__main__':
        return User.query.get(int(user_id))
