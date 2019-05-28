# -*- encoding: utf-8 -*-

import requests


# urllib 或 requests 两个库都可以发送请求
class HTTP(object):
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text





