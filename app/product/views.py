from . import product_blueprint
from flask import render_template, request, flash, redirect, url_for
from ..models import Product
from .forms import ProductAddForm, ProductFindForm, ProductEditForm, ProductImgAddForm
from app import db
from flask_login import login_required
from app.util import cos
from conf import Config


@product_blueprint.route("/new_product", methods=["GET", "POST"])
@login_required
def new_product():
    form = ProductAddForm()
    if form.validate_on_submit():
        Product.upload_product(form)
        return render_template("admin/products/add_products.html", form=form)
    return render_template("admin/products/add_products.html", form=form)


@product_blueprint.route("/find_products", methods=["GET", "POST"])
def find_products():
    form = ProductFindForm()
    page = request.args.get(key="page", default=1, type=int)
    limit = request.args.get(key="limit", default=12, type=int)
    search_name = request.args.get(key="search_name", default="")

    # 过滤器
    filters = dict()
    filters["language_id"] = request.args.get(key="product_language", type=int, default=-1)
    filters = {k: v for k, v in filters.items() if v != -1}

    # 分页查询
    paginate = (Product.query.filter(Product.name.like("%" + search_name + "%")).
                filter_by(**filters).
                order_by("id").
                paginate(page=page, per_page=limit)
                )

    items = paginate.items
    return render_template("products_list.html", items=items, pagination=paginate,
                           search_name=search_name, filter=filters, form=form)


@product_blueprint.route("/custom", methods=["GET"])
def custom():
    return render_template("custom.html")


@product_blueprint.route("/single_product", methods=["GET"])
def single_product():
    product_id = request.args.get("id", type=int)
    product = Product.query.filter_by(id=product_id).first()

    return render_template("single_product.html", product=product)


@product_blueprint.route("/edit_product", methods=["GET", "POST"])
@login_required
def edit_product():
    product_id = request.args.get("id", type=int)
    form = ProductEditForm()
    product = Product.query.filter_by(id=product_id).first()
    if form.validate_on_submit():
        product.name = form.name.data
        product.language_id = form.language.data
        product.is_doc = form.have_doc.data
        product.prices = form.prices.data
        product.description = form.description.data

        # 上传视频
        if form.video.data:
            product_video = form.video.data
            video_path = "{product_id}/{name}".format(product_id=product_id, name=product_video.filename)
            cos.upload_binary_file(binary_file=product_video, key=video_path)
            product.video_path = Config.COS_BUCKET_PATH + "/" + video_path

        db.session.add(product)
        db.session.commit()
        flash("修改成功!")

    form.id.data = product_id
    form.name.data = product.name
    form.description.data = product.description
    form.language.data = product.language_id
    form.have_doc.data = product.is_doc
    form.prices.data = int(product.prices)
    form.video.data = product.video_path
    form.imgs_path.data = product.imgs_path

    # 添加图片的Form
    img_add_form = ProductImgAddForm()
    img_add_form.id.data = product_id

    return render_template("admin/products/edit_product.html", form=form, img_add_form = img_add_form)


@product_blueprint.route("/add_imgs", methods=["POST","GET"])
@login_required
def add_imgs():
    """添加图片"""
    img_add_form = ProductImgAddForm()
    product_id = img_add_form.id.data
    if img_add_form.validate_on_submit():
        print("aaa")
        # 取出原始图片
        product = Product.query.filter_by(id=product_id).first()
        origin_imgs_path = product.imgs_path.split(";") if product.imgs_path else []

        # 上传图片
        add_imgs_path = list()  # 保存添加图片地址
        for img in img_add_form.imgs.data:
            img_path = "{id}/{filename}".format(id=product_id, filename=img.filename)
            add_imgs_path.append(img_path)
            cos.upload_binary_file(binary_file=img ,key=img_path)

        # 加入数据库
        add_imgs_path = list(map(lambda x: Config.COS_BUCKET_PATH + "/" + x, add_imgs_path))
        product.imgs_path = ";".join(origin_imgs_path + add_imgs_path)
        db.session.add(product)
        db.session.commit()
        flash("添加成功")

    return redirect(url_for("products.edit_product", id = product_id))