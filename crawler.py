#! /usr/bin/python3.6
# -*-coding:utf-8 -*-
"""
爬虫，用于爬取数据
"""

import re
import random
import logging
import requests
from requests.exceptions import ConnectionError
from scrapy.selector import Selector


class Proxymetaclass(type):
    """
    元类 把存在字符串crawl_的函数存入__CrawlFunc__之中
    _CrawlFuncCount__则保存个数
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []

        for k, v in attrs.items():
            # 仅仅以crawl_开头的作为爬取函数
            if k.startswith('crawl_'):
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count

        return type.__new__(cls, name, bases, attrs)


headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}


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

    def get_proxies(self, callback_name):
        """
        调用爬虫函数爬取代理
        :param callback_name: 爬虫函数
        :return:
        """
        proxies = set()
        for proxy in eval("self.{}()".format(callback_name)):
            proxies.add(proxy)
        return proxies

    def crawl_kuaidaili(self):
        """
        从快代理中爬取爬虫
        :return: 返回Proxy集
        """
        func_name = self.crawl_kuaidaili.__name__
        url_format = 'https://www.kuaidaili.com/free/inha/%d/'

        def callback(selector):
            tr_list = selector.css('table tbody tr')
            for tr in tr_list:
                ip = tr.css('[data-title="IP"]::text').extract_first()
                port = int(tr.css('[data-title="PORT"]::text').extract_first())
                yield ip, port
        return self._crawl_page(func_name, url_format, callback)

    def crawl_89ip(self):
        func_name = self.crawl_89ip.__name__
        url_format = 'http://www.89ip.cn/index_%d.html'

        def callback(selector):
            tr_list = selector.css('table tbody tr')
            for tr in tr_list:
                td_list = tr.css('td::text').extract()
                ip, port = td_list[0], int(td_list[1])
                yield ip, port
        return self._crawl_page(func_name, url_format, callback)

    def crawl_7yip(self):
        func_name = self.crawl_7yip.__name__
        url_format = 'https://www.7yip.cn/free/?action=china&page=%d'

        def callback(selector):
            tr_list = selector.css('table tbody tr')
            for tr in tr_list:
                ip = tr.css('[data-title="IP"]::text').extract_first()
                port = tr.css('[data-title="PORT"]::text').extract_first()
                yield ip, port

        return self._crawl_page(func_name, url_format, callback)

    def _crawl_page(self, func_name, url_format, callback):
        """
        从网络中爬取页面，并返回代理，
        :param func_name: 函数名称
        :param url_format: url
        :param callback: 解析函数
        :return: 如果爬取失败，返回None
        """
        page = self.get_static(func_name, 'page', 1)
        if page > 100:
            page = 1
        try:
            # 发送请求
            response = requests.get(url_format % page, headers=headers)
            # 获取代理
            selector = Selector(response)
            proxies = set()
            for ip, port in callback(selector):
                proxies.add('%s:%s' % (ip.strip(), port))
            # 回写变量
            self.set_static(func_name, 'page', page + 1)
            return proxies
        except (ConnectionError, ) as e:
            print(e.args)
        return None

    def get_static(self, func_name, key, default=None):
        """
        获取函数内的静态变量，key所对应的value，如果没有则返回default
        :param func_name: 函数名称
        :param key: 键
        :param default: 键对应的默认值
        :return: 返回键对应的值或default
        """
        if func_name not in self.variables:
            self.variables[func_name] = {key: default}
            return default
        elif key not in self.variables[func_name]:
            return default
        else:
            return self.variables[func_name][key]

    def set_static(self, func_name, key, value):
        """
        设置函数的静态变量，key=value
        :param func_name: 函数名称
        :param key: 键
        :param value: 值
        """
        if func_name not in self.variables:
            self.variables[func_name] = {key: value}
        else:
            self.variables[func_name][key] = value


if __name__ == '__main__':
    crawler = Crawler()
    # print(list(crawler.crawl_daili66()))
    print(crawler.crawl_89ip())
    # print(crawler.crawl_7yip())