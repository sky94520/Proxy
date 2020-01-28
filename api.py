#! /usr/bin/python3.6
# -*-coding:utf-8 -*-
"""
使用flask向外提供API
"""

from flask import Flask
from models import Proxy
import gunicorn

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    获取随机可用代理
    return: 返回一个字典，必然存在一个名称为status的键，如果为success，则可以直接获取proxy，
    否则根据msg来获取当前的错误
    """
    result = {'status': 'failure'}
    proxy = Proxy.random()
    if proxy is not None:
        result.update({'status': 'success', 'proxy': str(proxy)})
    else:
        result['msg'] = 'not enough available proxies'

    return result


@app.route('/count')
def get_counts():
    """
    获取代理池总量
    return :代理池总量
    """
    return str(Proxy.count())


if __name__ == '__main__':
    app.run()
