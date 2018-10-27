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
from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .. import email

from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from ..models import User
from .. import db


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.vertify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.admin")

            # 登录成功邮件提示
            email.send_email(
                to=current_app.config["ADMIN"],
                subject="用户登录成功",
                template="mail/login_success",
                user=user
            )
            return redirect(next)
        flash("Invalid username or password")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("You can now login.")
        return redirect(url_for("auth.login"))
    return render_template('auth/register.html', form=form)


@auth.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.vertify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your password has been updated")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid password")

    return render_template("auth/change_password.html", form=form)
