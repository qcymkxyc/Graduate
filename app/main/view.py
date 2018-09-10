#!/usr/bin/python3
# coding=utf-8

from . import main as main_blueprint
from flask import render_template

@main_blueprint.route("/")
def index():
    return render_template("index.html")
