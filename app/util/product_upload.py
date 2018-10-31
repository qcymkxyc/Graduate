#!/usr/bin/python3
# coding=utf-8
"""

@Time    : 18-10-30 下午4:05
@Author  : qcymkxyc
@Email   : qcymkxyc@163.com
@File    : product_upload.py
@Software: PyCharm

文件上传脚本

"""
import requests
import json
import os
import sys

description_filename = "descrition.txt"     # 描述的文件名
baidu_url_filename = "baidu.txt"    # 百度网盘分享存储文件名
images_foldername = "images"      # 图片文件夹
product_info_filename = "product_info.json"     # 保存产品信息

# upload_product_url = "www.yibangbishe.com.cn:8080/api/v1/new_product"   # 文件上传URL
upload_product_url = "http://localhost:5000/api/v1/new_product"   # 文件上传URL


def read_file(filename, mode="r"):
    """读取文本文件

    :param filename:str
        文件路径
    :param mode: str
        文件读取方式
    :return:str
        文本内容
    """
    with open(filename, mode, encoding="utf-8") as f:
        return f.read()


def upload_product(product_path):
    """上传产品信息

    :param product_path: str
        产品目录地址
    :raises:
        FileNotFoundError : 产品信息不存在
    """
    # 获取产品信息的绝对路径
    product_info_abs_filename = os.path.join(product_path, product_info_filename)

    # 产品信息文件不存在
    if not os.path.exists(product_info_abs_filename):
        raise FileNotFoundError("未发现产品信息文件")

    # 产品信息
    product_info = read_file(product_info_abs_filename)
    product_info = json.loads(product_info)

    # 取出上传文件
    files = [("imgs", open(img_path, "rb")) for img_path in product_info["imgs"]]
    files.append(("video", open(product_info["video"], "rb")))

    response = requests.post(upload_product_url, product_info, files=files)
    if response.status_code == 200 and json.loads(response.text)["msg"] == "success":
        print("{name}上传成功".format(name=product_info["name"]))
    else:
        print("{name}上传失败！".format(name=product_info.get("name")), file=sys.stderr)


def main():
    s = "/home/qcymkxyc/log/001ASP.NET学生管理系统3.0版"
    upload_product(s)


if __name__ == "__main__":
    main()
