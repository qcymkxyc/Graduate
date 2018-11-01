#!/usr/bin/python3
# coding=utf-8

from . import main as main_blueprint
from flask import render_template, abort, flash, redirect, url_for, send_from_directory, current_app
from flask_login import current_user, login_required
from ..models import User
from .form import EditProfileForm
from .. import db
from ..product.forms import ProductFindForm


@main_blueprint.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = ProductFindForm()
    return render_template("index.html", form=form)


@main_blueprint.route("/user/<username>")
def user(username):
    search_user = User.query.filter_by(name=username).first()
    if search_user is None:
        abort(404)
    return render_template("user.html", user=search_user)


@main_blueprint.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for(".user", username=current_user.name))

    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", form=form)


@main_blueprint.route("/<filename>")
def static_from_root(filename):
    """静态文件请求

    :param filename: str
        文件名
    """
    return send_from_directory(current_app.static_folder, filename)


@main_blueprint.route("/admin/<module_name>/<filename>")
def admin_file(module_name, filename):
    """请求后台管理页面

    :param filename: str
        后台页面名称
    :param module_name: str
        模块名
    :return: html
        后台页面
    """
    return render_template("admin/{module}/{filename}".format(module=module_name, filename=filename))
    # return send_from_directory("templates/admin/{module}".format(module=module_name), filename)
