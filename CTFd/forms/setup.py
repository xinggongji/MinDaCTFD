from flask_babel import lazy_gettext as _l
from wtforms import (
    FileField,
    HiddenField,
    IntegerField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired
from wtforms.widgets.html5 import NumberInput

from CTFd.constants.config import (
    AccountVisibilityTypes,
    ChallengeVisibilityTypes,
    RegistrationVisibilityTypes,
    ScoreVisibilityTypes,
)
from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.utils.config import get_themes


class SetupForm(BaseForm):
    ctf_name = StringField(
        "赛事名称", description="您的 CTF 赛事/活动的名称"
    )
    ctf_description = TextAreaField(
        "赛事描述", description="CTF 赛事的描述"
    )
    user_mode = RadioField(
        "用户模式",
        choices=[("teams", "团队模式"), ("users", "个人模式")],
        default="teams",
        description="选择参赛者是以团队形式（团队模式）还是个人形式（个人模式）参与比赛",
        validators=[InputRequired()],
    )

    name = StringField(
        "管理员用户名",
        description="管理员账户的用户名",
        validators=[InputRequired()],
    )
    email = EmailField(
        "管理员邮箱",
        description="管理员账户的邮箱地址",
        validators=[InputRequired()],
    )
    password = PasswordField(
        "管理员密码",
        description="管理员账户的密码",
        validators=[InputRequired()],
    )

    ctf_logo = FileField(
        "Logo 图标",
        description="网站 Logo，用于替代赛事名称显示在首页按钮位置。可选。",
    )
    ctf_banner = FileField(
        "横幅", description="首页横幅图片。可选。"
    )
    ctf_small_icon = FileField(
        "小图标",
        description="浏览器标签页图标 favicon。仅支持 PNG 格式，需 32x32 像素。可选。",
    )
    ctf_theme = SelectField(
        "主题",
        description="CTFd 使用的主题，可后期更改。",
        choices=list(zip(get_themes(), get_themes())),
        ## TODO: Replace back to DEFAULT_THEME (aka core) in CTFd 4.0
        default="core-beta",
        validators=[InputRequired()],
    )
    theme_color = HiddenField(
        "主题颜色",
        description="主题使用的颜色，控制外观风格。需要主题支持。可选。",
    )

    verify_emails = SelectField(
        "验证邮箱",
        description="控制用户是否必须确认邮箱地址才能参赛",
        choices=[("true", "启用"), ("false", "禁用")],
        default="false",
    )
    team_size = IntegerField(
        widget=NumberInput(min=0),
        description="每个团队的用户数量（仅团队模式）。可选。",
    )
    challenge_visibility = SelectField(
        "题目可见性",
        description="控制用户是否需要登录才能查看题目",
        choices=[
            (ChallengeVisibilityTypes.PUBLIC, "公开"),
            (ChallengeVisibilityTypes.PRIVATE, "仅登录"),
            (ChallengeVisibilityTypes.ADMINS, "仅管理员"),
        ],
        default=ChallengeVisibilityTypes.PRIVATE,
    )
    account_visibility = SelectField(
        "账户可见性",
        description="控制账户（用户和团队）对所有人、仅认证用户、或仅管理员可见",
        choices=[
            (AccountVisibilityTypes.PUBLIC, "公开"),
            (AccountVisibilityTypes.PRIVATE, "仅登录"),
            (AccountVisibilityTypes.ADMINS, "仅管理员"),
        ],
        default=AccountVisibilityTypes.PUBLIC,
    )
    score_visibility = SelectField(
        "分数可见性",
        description="控制解题/分数对公开、登录用户、非管理员隐藏、或仅管理员可见",
        choices=[
            (ScoreVisibilityTypes.PUBLIC, "公开"),
            (ScoreVisibilityTypes.PRIVATE, "仅登录"),
            (ScoreVisibilityTypes.HIDDEN, "隐藏"),
            (ScoreVisibilityTypes.ADMINS, "仅管理员"),
        ],
        default=AccountVisibilityTypes.PUBLIC,
    )
    registration_visibility = SelectField(
        "注册可见性",
        description="控制注册是否对所有人开放或已关闭",
        choices=[
            (RegistrationVisibilityTypes.PUBLIC, "公开"),
            (RegistrationVisibilityTypes.PRIVATE, "关闭"),
            (RegistrationVisibilityTypes.MLC, "仅 MajorLeagueCyber"),
        ],
        default=RegistrationVisibilityTypes.PUBLIC,
    )

    start = StringField(
        "开始时间",
        description="CTF 计划开始的时间。可选。",
    )
    end = StringField(
        "结束时间",
        description=_l("Time when your CTF is scheduled to end. Optional."),
    )
    submit = SubmitField(_l("Finish"))
