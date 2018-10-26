#!/usr/bin/python3
# coding=utf-8
"""

@Time    : 18-10-17 下午3:51
@Author  : qcymkxyc
@Email   : qcymkxyc@163.com
@File    : wsgi.py
@Software: PyCharm
    
"""
from app import create_app

application = create_app(config_name="production")

if __name__ == "__main__":
    application.run()
