#!/usr/bin/python3
# coding=utf-8
"""

@Time    : 18-10-8 下午3:45
@Author  : qcymkxyc
@Email   : qcymkxyc@163.com
@File    : cos.py
@Software: PyCharm

腾讯云cos
    
"""
import conf
from app import cos_client

def upload_binary_file(binary_file,key,bucket = conf.Config.COS_BUCKET,client = cos_client):
    """上传二进制文件到腾讯云

    :param binary_file: binary
        二进制文件
    :param key: str
        上传后的文件名，该文件名可包含路径，比如/test/test.mp4
    :param bucket: str
        Bucket名
    :param client: q_cloud_cos.Cos3Client
        上传的客户端对象
    :return:
        上传文件的MD5码
    """
    response = client.put_object(
        Bucket=bucket,
        Body = binary_file,
        Key=key
    )
    return response["ETag"]

