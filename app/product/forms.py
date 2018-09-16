from flask_wtf import Form
from wtforms import SubmitField,StringField,TextAreaField,SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileRequired,FileAllowed

class ProductAddForm(Form):
    name = StringField("毕业设计题目",[DataRequired])
    description = TextAreaField(label = "毕业设计描述",validators = [DataRequired()])

    language = SelectField(
        label = "语言",
        choices = {
            (1,"JAVA"),
            (2,"C#"),
            (3,"PHP"),
            (4,"C语言"),
            (5,"Python"),
            (6,"神经网络")
        }),

    video = FileField(label = "视频",validators = [
        FileAllowed(["mp4","avi","ogg"],message = "mp4/avi allowed")
    ])
    submit = SubmitField("提交")