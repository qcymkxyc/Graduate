from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, SelectField
from wtforms import HiddenField, RadioField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from ..models import Language
from .. import products_video, products_images


class ProductAddForm(FlaskForm):
    name = StringField("毕设题目", [DataRequired()])
    description = TextAreaField(label="毕业设计描述", validators=[DataRequired()])
    language = SelectField(label="语言", coerce=int)
    imgs = MultipleFileField(label="图片",
                             validators=[FileAllowed(products_images, "Image Only")]
                             )
    video = FileField(label="视频", validators=[
        FileAllowed(products_video, message="mp4/avi allowed")
    ])
    have_doc = RadioField(
        label="是否有论文",
        choices=[(True, "是"), (False, "否")],
        coerce=bool,
        default=False
    )
    price = IntegerField(
        label="价格",
        validators=[DataRequired()]
    )
    baidu_url = StringField(label="百度URL", validators=[DataRequired()])
    submit = SubmitField("提交")

    def __init__(self):
        super(ProductAddForm, self).__init__()
        self.language.choices = [(single_language.id, single_language.name) for single_language in Language.query.all()]


class ProductFindForm(FlaskForm):
    search_name = StringField(label="商品名")
    language = SelectField(label="语言", coerce=int)
    have_doc = SelectField(label="是否有论文", choices=[(-1, "无限制"), (1, "是"), (0, "否")], default=-1, coerce=int)
    have_img = SelectField(label="是否有图片", choices=[(-1, "无限制"), (1, "是"), (0, "否")], default=-1, coerce=int)
    have_video = SelectField(label="是否有视频", choices=[(-1, "无限制"), (1, "是"), (0, "否")], default=-1, coerce=int)

    submit = SubmitField("查询")

    def __init__(self):
        super(ProductFindForm, self).__init__()
        self.language.choices = [(single_language.id, single_language.name) for single_language in Language.query.all()]
        self.language.choices.insert(0, (-1, "无限制"))


class ProductEditForm(FlaskForm):
    id = StringField(label="ID")
    name = StringField(label="商品名")
    description = TextAreaField(label="描述")
    language = SelectField(label="语言", coerce=int)
    have_doc = SelectField(label="是否有论文", choices=[(1, "是"), (0, "否")], coerce=int)
    prices = IntegerField(label="价格")

    video = FileField(label="视频", validators=[
        FileAllowed(products_video, message="mp4/avi allowed")
    ])
    imgs_path = HiddenField(label="IMGS")

    submit = SubmitField("修改")

    def __init__(self):
        super(ProductEditForm, self).__init__()
        self.language.choices = [(single_language.id, single_language.name) for single_language in Language.query.all()]


class ProductImgAddForm(FlaskForm):
    """添加商品图片"""

    id = HiddenField(label="ID")
    imgs = MultipleFileField(label="选择要添加的图片",
                             validators=[FileAllowed(products_images, "Image Only")]
    )
    submit = SubmitField("确定")
