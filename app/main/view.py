#!/usr/bin/python3
# coding=utf-8

from . import main as main_blueprint
from flask import render_template, abort, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import User
from .form import EditProfileForm
from .. import db
from ..product.forms import ProductFindForm


@main_blueprint.route("/admin")
def admin():
    return render_template("admin.html")


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = ProductFindForm()
    return render_template("index.html", form=form)


@main_blueprint.route("/user/<username>")
def user(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        abort(404)
    return render_template("user.html", user=user)


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
        print(current_user.name)
        return redirect(url_for(".user", username=current_user.name))

    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", form=form)


@main_blueprint.route("/baidu_verify_L2SVVu2dc7.html", methods=["GET"])
def baidu_vertify():
    return render_template("baidu_verify_L2SVVu2dc7.html")


# @main_blueprint.route("/edit-profile/<int:id>")
# @login_required
# # @ad
# def edit_profile_admin(id):
#     user = User.query.get


