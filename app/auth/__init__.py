#!/usr/bin/python3
# coding=utf-8
"""

 @Time    : 18-8-26 下午8:15
 @Author  : qcymkxyc
 @Email   : qcymkxyc@163.com
 @File    : __init__.py.py
 @Software: PyCharm
    
"""
from flask.blueprints import Blueprint

auth = Blueprint("auth",__name__)

from . import  views,forms