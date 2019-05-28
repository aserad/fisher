# -*- encoding: utf-8 -*-

from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(message='邮箱不能为空'), Length(8, 64),
                                    Email(message='电子邮箱格式不正确')])

    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])

    nickname = StringField(validators=[DataRequired(message='昵称不能为空'),
                                       Length(2, 10, message='昵称至少需要2个字符，最多10个字符')])

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError("该邮箱已被注册")

    def validate_nickname(self, field):
        user = User.query.filter_by(nickname=field.data).first()
        if user is not None:
            raise ValidationError("该昵称已被使用    ")


class LoginForm(Form):
    email = StringField(validators=[DataRequired(message='邮箱不能为空'), Length(8, 64),
                                    Email(message='电子邮箱格式不正确')])

    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(message='邮箱不能为空'), Length(8, 64),
                                    Email(message='电子邮箱格式不正确')])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(message='密码不能为空'),
        Length(6, 32, message='密码长度必须在6到32个字符之间'),
        EqualTo('password2', message='两次输入的密码不一致')])

    password2 = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])
