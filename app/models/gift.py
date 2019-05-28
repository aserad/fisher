# -*- encoding: utf-8 -*-
from flask import current_app
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook
from collections import namedtuple


EachGiftWishCount = namedtuple('EachGiftWishCount', ['isbn', 'count'])


class Gift(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    isbn = Column(String(15), nullable=False)

    def is_self_gift(self, uid):
        return True if uid == self.uid else False

    @classmethod
    def recent(cls):
        # 链式调用
        # 主体 Query
        # 子函数
        # first() all()  # 最终执行查询
        recent_gifts = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).all()
        return recent_gifts

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 到wish表中计算出某个礼物的wish心愿数量
        count_list = db.session.query(Wish.isbn, func.count(Wish.id)).filter(
            Wish.launched is False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{"isbn": w[0], "count": w[1]} for w in count_list]
        return count_list
