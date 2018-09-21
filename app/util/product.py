from flask import current_app
from .. import products_video,products_images
import os

def save_product(product_form,product):
    """
    保存商品的图片及视频
    :param product_form: 商品的form
    :param product: Product类
    """
    product_name = product_form.name.data

    img1 = product_form.img1.data
    img2 = product_form.img2.data
    img3 = product_form.img3.data

    video = product_form.video.data

    img_base_path = current_app.config["UPLOADED_IMAGE_DEST"]
    video_base_path = current_app.config["UPLOADED_VIDEO_DEST"]

    img1_path = products_images.save(folder=product_name,storage=img1)
    img2_path = products_images.save(folder=product_name,storage=img2)
    img3_path = products_images.save(folder=product_name,storage=img3)
    video_path = products_video.save(folder=product_name,storage=video)

    product.picture1_path = os.path.join(img_base_path,img1_path)
    product.picture2_path = os.path.join(img_base_path,img2_path)
    product.picture3_path = os.path.join(img_base_path,img3_path)

    product.video_path = os.path.join(video_base_path,video_path)

