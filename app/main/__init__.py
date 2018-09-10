#!/usr/bin/python3
# coding=utf-8

from flask import blueprints

main = blueprints.Blueprint("main",__name__)

from . import view,error,form

