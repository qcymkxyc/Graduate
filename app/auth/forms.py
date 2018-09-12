#!/usr/bin/python3
# coding=utf-8
"""

 @Time    : 18-8-30 下午7:58
 @Author  : qcymkxyc
 @Email   : qcymkxyc@163.com
 @File    : forms.py
 @Software: PyCharm
    
"""
from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField,ValidationError
from wtforms.validators import Required,Length,Email,EqualTo,DataRequired
from ..models import User

class LoginForm(Form):
    email = StringField("Email",validators = [Required(),Length(1,64),Email()])
    password = PasswordField("Password",validators = [Required()])
    remember_me = BooleanField("keep me logged in")
    submit = SubmitField("Log in")


class RegistrationForm(Form):
    email = StringField("Email",validators=[Required(),Length(1,64),Email()])
    username = StringField("Username",validators=[Required(),Length(1,64)])
    password2 = PasswordField("Confirm Password", validators=[Required()])
    password = PasswordField("Password",validators=[Required(),EqualTo('password2',"Password must match")])
    submit = SubmitField("Register")

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")

    def validate_username(self,field):
        if User.query.filter_by(name = field.data).first():
            raise ValidationError("Username already in use.")


class ChangePasswordForm(Form):
    old_password = PasswordField("Your Old Password",validators = [Required()])
    password = PasswordField("New Password",validators = [Required(),EqualTo("password2","Password must match")])
    password2 = PasswordField("Confirm New Password",validators = [Required()])

    submit = SubmitField("Update Password")

