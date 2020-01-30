#! /usr/bin/python3.6
# -*-coding:utf-8 -*-
"""
爬虫，用于爬取数据
"""

import re
import random
import logging
import requests
from scrapy.selector import Selector
from models import Proxy


class Proxymetaclass(type):
    """
    元类 把存在字符串crawl_的函数存入__CrawlFunc__之中
    _CrawlFuncCount__则保存个数
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []

        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count

        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=Proxymetaclass):
    """
    爬虫类，每一个带有crawl_方法的函数都认为是爬虫函数，
    该函数需要yiled等返回"ip:port"对应的代理地址
    """
    def __init__(self):
        # 正则提取IP地址+端口号
        self.pattern = re.compile(r'\d+\.\d+\.\d+\.\d+:\d+')
        # 存储函数变量
        self.variables = {}

    def get_proxies(self, callback):
        """
        通过爬虫爬取代理
        :param callback: 爬虫函数
        :return:
        """
        proxies = []

        for proxy in eval("self.{}()".format(callback)):
            print('Successfully get proxy', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self):
        """
        获取代理66
        return 代理
        """
        url = 'http://www.66ip.cn/nmtq.php'
        params = {
            'getnum': None,
            'isp': 0,
            'anonymoustype': 3,
            'start': None,
            'ports': None,
            'export': None,
            'ipaddress': None,
            'area': 0,
            'proxytype': 0,
            'api': '66ip'
        }
        try:
            response = requests.get(url, params=params)
            text = response.text
            # get_page(url, params=params)
            results = re.findall(self.pattern, text)
            # 所有的列表整合成一个列表
            for result in results:
                yield result
        except Exception as e:
            logging.error(e)
        return None

    def crawl_kuaidaili(self):
        """
        从快代理中爬取爬虫
        :return: 返回Proxy集
        """
        proxies = set()
        page = self.get_static(self.crawl_kuaidaili, 'page', 1)
        # 发送请求
        response = requests.get('https://www.kuaidaili.com/free/inha/%d/' % page)
        # 获取代理
        selector = Selector(response)
        tr_list = selector.css('table tbody tr')
        for tr in tr_list:
            ip = tr.css('[data-title="IP"]::text').extract_first()
            port = int(tr.css('[data-title="PORT"]::text').extract_first())
            proxies.add(Proxy(ip=ip, port=port))
        # 回写变量
        self.set_static(self.crawl_kuaidaili, 'page', page + 1)
        return proxies

    def get_static(self, func, key, default=None):
        """
        获取函数内的静态变量，key所对应的value，如果没有则返回default
        :param func: 函数
        :param key: 键
        :param default: 键对应的默认值
        :return: 返回键对应的值或default
        """
        name = func.__name__
        if name not in self.variables:
            self.variables[name] = {key: default}
            return default
        elif key not in self.variables[name]:
            return default
        else:
            return self.variables[name][key]

    def set_static(self, func, key, value):
        """
        设置函数的静态变量，key=value
        :param func: 函数
        :param key: 键
        :param value: 值
        """
        name = func.__name__
        if name not in self.variables:
            self.variables[name] = {key: value}
        else:
            self.variables[name][key] = value


if __name__ == '__main__':
    crawler = Crawler()
    # print(list(crawler.crawl_daili66()))
    crawler.crawl_kuaidaili()
