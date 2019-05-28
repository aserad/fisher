# -*- encoding: utf-8 -*-

from flask import Flask, current_app, request, g

app = Flask(__name__)


# ctx = app.app_context()
# ctx.push()
# a = current_app
# d = current_app.config['DEBUG']
# print(d)
# ctx.pop()


# with app.app_context():
#     a = current_app
#     d = current_app.config['DEBUG']
#     print(d)


class ContextText:
    def __enter__(self):
        print('connect to resource')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """返回值只有 True 或 False , 当返回值为True时，外部不会抛出异常"""
        if exc_tb:
            print('process exception')
        else:
            print('no exception')
        print('close resource connect')
        return True

    def query(self):
        print('query data')


with ContextText() as res:
    res.query()
