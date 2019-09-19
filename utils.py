#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}


def get_page(url, **kwargs):
    """
    从url中获取html文本
    @param url 链接
    return 获取到的文本
    """
    response = requests.get(url, headers=headers, **kwargs)

    if response.status_code == requests.codes.ok:
        return response.text
    return None
