#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

from flask import Flask, g
from db import RedisClient
from redis.exceptions import DataError
import gunicorn

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


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
    conn = get_conn()
    try:
        proxy = conn.random()
        result.update({'status': 'success', 'proxy': proxy})
    except DataError:
        result['msg'] = 'not enough available proxies'

    return result


@app.route('/count')
def get_counts():
    """
    获取代理池总量
    return :代理池总量
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()
