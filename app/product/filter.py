#!/usr/bin/python3
# coding=utf-8
"""

@Time    : 18-10-24 下午3:33
@Author  : qcymkxyc
@Email   : qcymkxyc@163.com
@File    : filter.py
@Software: PyCharm

过滤器

"""
import re


def cos_picc_filter(img_path):
    """把COS地址转换为PICC（数据万象）地址,用于jinja2中的自定义filter

    :param img_path: str
        图片地址
    :return: str
        转换后的地址
    """
    pattern = "cos\.ap-.+?\."
    return re.sub(pattern, "piccd.", img_path)

# a = "http://graduate-1253764997.cos.ap-chengdu.myqcloud.com/658/index_01."
cos_picc_filter("")