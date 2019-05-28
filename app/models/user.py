# -*- encoding: utf-8 -*-
from math import floor

from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float

from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app import login_manager
from app.models.base import Base, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login.mixins import UserMixin

from app.models.drift import Drift
from app.spider.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(Base, UserMixin):
    # __tablename__ = 'user1'   # 指定表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128))
    email = Column(String(50), nullable=False, unique=True)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.SUCCESS).count()
        if floor(success_receive_count / 2) <= floor(success_gifts_count):
            return True
        return False

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        """判断是否能添加到赠送清单"""
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        # 用户赠送的图书要存在
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不能同时成为赠送者和索要者

        # 既不在赠送清单也不再心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({"id": self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=f'{self.send_counter}/{self.receive_counter}'
        )

    # def get_id(self):  # 如果字段不是id，就要重写该方法
    #     return self.id


@login_manager.user_loader
def get_user(uid):
    user = User.query.get(int(uid))
    return user

