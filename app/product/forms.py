from flask_wtf import Form
from wtforms import SubmitField,StringField,TextAreaField,SelectField,RadioField,IntegerField,MultipleFileField
from wtforms.validators import DataRequired,NumberRange,URL
from flask_wtf.file import FileField,FileAllowed
from ..models import Language
from .. import products_video,products_images


class ProductAddForm(Form):
    name = StringField("毕设题目", [DataRequired()])
    description = TextAreaField(label="毕业设计描述", validators=[DataRequired()])
    language = SelectField(label="语言", coerce=int)
    imgs = MultipleFileField(label="图片", validators=[FileAllowed(products_images, "Image Only")])
    video = FileField(label="视频", validators=[
        FileAllowed(products_video, message="mp4/avi allowed")
    ])
    have_doc = RadioField(
        label="是否有论文",
        choices=[
            (True, "是"),
            (False, "否")
        ],
        coerce=bool,
        default=False
    )
    price = IntegerField(
        label="价格",
        validators=[
            NumberRange(min=0, max=2000, message="价格必须在0 - 2000之间")
        ]
    )
    baidu_url = StringField(
        label="百度URL",
        validators=[
            URL(message = "字段必须为URL")
        ]
    )
    submit = SubmitField("提交")

    def __init__(self):
        super(ProductAddForm,self).__init__()
        self.language.choices = [(single_language.id,single_language.name) for single_language in Language.query.all()]


class ProductFindForm(Form):
    name = StringField(label="商品名")
    language = SelectField(
        label = "语言",
        coerce=int
    )
    have_doc = SelectField(
        label = "是否有论文",
        choices = [
            (-1,"无限制"),
            (1,"是"),
            (0,"否")
        ],
        default = -1,
        coerce=int
    )
    have_img = SelectField(
        label = "是否有图片",
        choices=[
            (-1,"无限制"),
            (1,"是"),
            (0,"否")
        ],
        default=-1,
        coerce=int
    )
    have_video = SelectField(
        label = "是否有视频",
        choices=[
            (-1,"无限制"),
            (1,"是"),
            (0,"否")
        ],
        default=-1,
        coerce=int
    )

    submit = SubmitField("查询")

    def __init__(self):
        super(ProductFindForm, self).__init__()
        self.language.choices = [(single_language.id, single_language.name) for single_language in Language.query.all()]

