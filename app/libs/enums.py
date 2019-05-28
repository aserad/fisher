# -*- encoding: utf-8 -*-
from enum import Enum


class PendingStatus(Enum):
    """交易状态"""
    WAITING = 1
    SUCCESS = 2
    REJECT = 3
    REDRAW = 4

    @classmethod
    def pending_str(cls, status, key):
        key_map = {
            cls.WAITING: {
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄',
            },
            cls.REJECT: {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝',
            },
            cls.REDRAW: {
                'requester': '你已撤消',
                'gifter': '对方已撤消',
            },
            cls.SUCCESS: {
                'requester': '对方已邮寄',
                'gifter': '你已邮寄，交易完成',
            },
        }
        return key_map[status][key]
