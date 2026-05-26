from wtforms import (
    BooleanField,
    HiddenField,
    MultipleFileField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm


class PageEditForm(BaseForm):
    title = StringField(
        "标题", description="页面标题，显示在导航栏中"
    )
    route = StringField(
        "路由",
        description="页面的 URL 路由（例如 /page），也可以输入链接地址",
    )
    draft = BooleanField("草稿")
    hidden = BooleanField("隐藏")
    auth_required = BooleanField("需要登录")
    content = TextAreaField("内容")
    format = SelectField(
        "格式",
        choices=[("html", "HTML")],
        default="html",
        validators=[InputRequired()],
        description="页面渲染格式",
    )
    link_target = SelectField(
        "打开方式",
        choices=[("", "当前页面"), ("_blank", "新标签页")],
        default="",
        validators=[],
        description="页面打开的目标位置",
    )


class PageFilesUploadForm(BaseForm):
    file = MultipleFileField(
        "上传文件",
        description="使用 Ctrl+点击 或 Cmd+点击 附加多个文件",
        validators=[InputRequired()],
    )
    type = HiddenField("页面类型", default="page", validators=[InputRequired()])
