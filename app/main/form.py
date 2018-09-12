#!/usr/bin/python3
# coding=utf-8

from flask_wtf import Form
from wtforms import StringField,TextAreaField,SubmitField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Email
from wtforms import ValidationError
from ..models import User,Role

class EditProfileForm(Form):
    name = StringField("Real name",validators=[Length(0,64)])
    location = StringField("Location",validators=[Length(0,64)])
    about_me = TextAreaField("About me")
    submit = SubmitField("Submit")


class EditProfileAdminForm(Form):
    email = StringField("Email",validators = [DataRequired(),Length(1,64),Email()])
    username = StringField("Username",validators = [DataRequired(),Length(1,64)])
    confirmed = BooleanField("Confirmed")

    role = SelectField("Role",coerce=int)
    name = StringField("Real Name",validators = [DataRequired(),Length(0,64)])
    location = StringField("Location",validators = [Length(0,64)])
    about_me = TextAreaField("About me")
    submit = SubmitField("Submit")

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self,field):
        if field.data != self.user.email and User.query.filter_by(email = field.data).first():
            raise ValidationError("Email already registered")

    def validate_username(self,field):
        if field.data != self.user.name and User.query.filter_by(name = field.data).first():
            raise ValidationError("Username already in user")
