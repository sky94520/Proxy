#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

from utils import get_page
import re


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

    def get_proxies(self, callback):
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
            'anonymoustype': 0,
            'start': None,
            'ports': None,
            'export': None,
            'ipaddress': None,
            'area': 0,
            'proxytype': 2,
            'api': '66ip'
        }
        try:
            text = get_page(url, params=params)
            results = re.findall(self.pattern, text)
            # 所有的列表整合成一个列表
            for result in results:
                yield result
        except Exception as e:
            print(e)
        return None


if __name__ == '__main__':
    crawler = Crawler()

    print(list(crawler.crawl_daili66()))
