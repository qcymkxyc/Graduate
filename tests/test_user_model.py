#!/usr/bin/python3
# coding=utf-8
"""

 @Time    : 18-8-26 下午7:40
 @Author  : qcymkxyc
 @Email   : qcymkxyc@163.com
 @File    : test_user_model.py
 @Software: PyCharm
    
"""
import unittest
from app.models import User
from app import db

class UserModelTestCase(unittest.TestCase):
    """测试用户Model"""
    def setUp(self):
        self.user = User()
        self.user.password = "cat"

    def test_password_setter(self):
        self.assertTrue(self.user.hash_password is not None)

    def test_password_getter(self):
        with self.assertRaises(AttributeError) :
            self.user.password

    def test_password_vertify(self):
        self.assertTrue(self.user.vertify_password("cat"))
        self.assertFalse(self.user.vertify_password("dog"))

    def test_user_add(self):
        self.user.email = "123456@qq.com"
        self.user.password = "123456"
        self.user.name = "aaa"
        db.session.add(self.user)
        db.session.commit()


    def test_password_hash(self):
        u2 = User(password = "dog")
        self.assertNotEqual(self.user.hash_password,u2.hash_password)


