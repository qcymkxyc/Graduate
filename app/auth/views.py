#!/usr/bin/python3
# coding=utf-8
"""

 @Time    : 18-8-30 下午7:38
 @Author  : qcymkxyc
 @Email   : qcymkxyc@163.com
 @File    : views.py
 @Software: PyCharm
    
"""
from . import auth
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user

from .forms import LoginForm
from ..models import User

@auth.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.vertify_password(form.password.data):
            login_user(user,form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("Invalid username or password")
    return render_template("/auth/login.html",form=form)

@login_required
@auth.route("/logout")
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("main.index"))
