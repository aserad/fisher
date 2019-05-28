# -*- encoding: utf-8 -*-
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    # Python email
    # msg = Message('测试邮件', sender='2477947149@qq.com', body='test', recipients=['aserad@163.com'])
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    app_ = current_app._get_current_object()
    t = Thread(target=send_async_email, args=[app_, msg])
    t.start()
    # mail.send(msg)
