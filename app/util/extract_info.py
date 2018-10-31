# coding=utf-8
import os
import zipfile
import argparse
import json

description_filename = "descrition.txt"     # 描述的文件名
baidu_url_filename = "baidu.txt"    # 百度网盘分享存储文件名
images_foldername = "images"      # 图片文件夹
product_info_filename = "product_info.json"     # 保存产品信息


def pre_process(base_path):
    """提取信息的预处理

    :param base_path:str
        基路径
    """
    for product_name in os.walk(base_path):
        product_path = os.path.join(base_path, product_name)
        # 创建图片文件夹
        image_absfolder_path = os.path.join(product_path, images_foldername)
        if not os.path.exists(image_absfolder_path):
            os.mkdir(image_absfolder_path)
        # 百度网盘保存文件
        baidu_url_absfilepath = os.path.join(product_path, baidu_url_filename)
        if not os.path.exists(baidu_url_absfilepath):
            write_file(baidu_url_absfilepath, {})
        # 描述文件
        description_absfilepath = os.path.join(product_path, description_filename)
        if not os.path.exists(description_absfilepath):
            write_file(description_absfilepath, {})


def read_file(filename):
    """读取文本文件

    :param filename:str
        文件路径
    :return:str
        文本内容
    """
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filename, info_dict):
    """写入文本写入文件

    :param filename: str
        文件路径
    :param info_dict:dict
        文本字典
    :raises:
        TypeError : 写入信息必须为字典类型
    """
    if not isinstance(info_dict, dict):
        raise TypeError("写入信息必须为字典类型")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(info_dict,fp=f,indent=4,ensure_ascii=False)


# 获取项目名
def process_product_name(filename):
    """获取项目名
    :param filename: str
        项目路径
    :return: str
        项目名
    """
    _, dirname = os.path.split(filename)
    product_name = dirname
    return product_name


# 项目描述
def process_description(filename):
    """获取项目描述(找文件夹下的新建文本文档文件，如未找到则返回空字符串)

    :param filename:str
        项目路径
    :return: str
         项目描述
    """
    try:
        description = read_file(os.path.join(filename, description_filename))
    except FileNotFoundError:
        description = ""
    return description


# 项目语言
languages = {
    "java": 1,
    "C#": 2,
    "PHP": 3,
    "C": 4,
    "Python": 5,
    "其他": 6,
    "VB": 7}
language_suffix = {
    "C#": ("cs",),
    "java": ("java", "jsp"),
    "PHP": ("php",),
    "C": ("cpp",),
    "Python": ("py",),
    "VB": ("vb",)
}


def process_language(filename):
    """获取语言

    :param filename:str
        项目路径
    :return: int
        语言对应的值
    """
    product_language = None
    is_stop = False
    for root, dirs, files in os.walk(filename):
        for full_filename in files:
            # 无后缀名的情况
            try:
                sub_filename, suffix = full_filename.split(sep=".", maxsplit=1)
            except ValueError:
                continue
            else:
                for language_name, suffixes in language_suffix.items():
                    if suffix in suffixes:
                        product_language = language_name
                        is_stop = True
                        break
        if is_stop:
            break
    # 没找到匹配则为其他
    if not product_language:
        product_language = "其他"

    language_value = languages.get(product_language)
    return language_value


# 是否有文档
def process_is_doc(filename):
    """是否有文档（找doc和docx后缀的文档）

    :param filename:str
        文件路径
    :return: bool
         是否有文档
    """
    is_doc = False
    for root, dirs, files in os.walk(filename):
        for f in files:
            if f.endswith("doc") or f.endswith("docx"):
                is_doc = True
                break
    return is_doc


# 百度网盘地址
def process_baidu_url(filename):
    """返回百度网盘地址

    :param filename:str
        项目路径
    :return:str
        百度网盘分享url及密码
    """
    try:
        baidu_url = read_file(os.path.join(filename, baidu_url_filename))
    except FileNotFoundError:
        baidu_url = ""
    return baidu_url


# 价格
def process_price():
    """返回价格

    :return: int
        价格
    """
    price = 100.
    return price


def process_images(product_path):
    """提取图片路径（项目路径下的image文件夹）

    :param product_path:str
        商品路径
    :return: list
        上传的图片路径
    """
    image_foler = os.path.join(product_path, images_foldername)
    image_pathes = list()

    # 如果没有提取图片
    if not os.path.exists(image_foler):
        return image_pathes

    for image_name in os.listdir(image_foler):
        image_path = os.path.join(image_foler, image_name)
        # 确认是图片文件
        if (os.path.isfile(image_path) and
                (image_name.endswith("png") or image_name.endswith("jpg"))):
            image_pathes.append(image_path)
    return image_pathes


def process_video(product_path):
    """提取视频路径（mp4）

    :param product_path:str
        产品路径
    :return: str
        视频路径
    """
    for filename in os.listdir(product_path):
        if os.path.isfile(os.path.join(product_path, filename)):
            if filename.endswith("mp4"):
                return os.path.join(product_path, filename)

    return ""


def process_product_info(product_path, info_path=None):
    """生成项目文档

    :param product_path: str
         项目路径
    :param info_path: str
        保存文档路径
    """
    product_path.replace("\\", "\\\\")
    if not info_path:
        info_path = product_path

    product_info = {
        "name": process_product_name(product_path),
        "description": process_description(product_path),
        "language": process_language(product_path),
        "have_doc": process_is_doc(product_path),
        "price": process_price(),
        "baidu_url": process_baidu_url(product_path),
        "imgs": process_images(product_path),
        "video": process_video(product_path)
    }

    write_file(os.path.join(info_path, product_info_filename), product_info)


def process_all_product_info(base_path=None):
    """提取总目录下的所有项目信息

    :param base_path:str
        放成品的总目录
    """
    if not base_path:
        base_path = os.getcwd()
    for product_path in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, product_path)):
            process_product_info(os.path.join(base_path, product_path))


def zip_product(product_name):
    """

    :param product_name:
    :return:
    """
    pass


def main():
    # parse = argparse.ArgumentParser(description="项目信息提取命令行工具")
    # parse.add_argument("extract-info",help="提取文件信息")
    # parse.parse_args()
    s = "/home/qcymkxyc/log/001ASP.NET学生管理系统3.0版"
    process_product_info(s)


if __name__ == "__main__":
    s = r"F:\mystyle\working\\成品整理\\001ASP.NET学生管理系统3.0版"
    # process_product_info(s)
    # main("F:\mystyle\working\\成品整理\\")
    # print(os.getcwd())
    # process_all_product_info(r"F:\mystyle\working\\成品整理")
    # pre_process(s)
    main()
