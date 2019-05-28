# -*- encoding: utf-8 -*-

from flask import Flask
from flask_mail import Mail

from app.models.base import db
from flask_login import LoginManager
from app.libs.limiter import Limiter

login_manager = LoginManager()
mail = Mail()
limiter = Limiter()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    mail.init_app(app)

    # 方法1
    # db.create_all(app=app)
    # 方法2
    with app.app_context():
        db.create_all()

    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
