#! /usr/bin/python3.6
# -*-coding:utf-8 -*-
"""
负责调用爬虫
"""

from crawler import Crawler
from settings import POOL_UPPER_THRESHOLD
from models import Proxy
import log
import logging


class Getter(object):
    """
    根据阈值判断是否爬取
    """
    def __init__(self):
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        return Proxy.count() >= POOL_UPPER_THRESHOLD

    def run(self):
        if not self.is_over_threshold():
            logging.info('Getter now running')
            old_count = Proxy.count()
            # 调用爬虫方法
            for callback in self.crawler.__CrawlFunc__:
                # 尝试爬取全部的数据
                proxies = self.crawler.get_proxies(callback)

                Proxy.add(proxies)
                if self.is_over_threshold():
                    break
                # 未爬取到数据
                if old_count == Proxy.count():
                    logging.error('%s function can\'t crawl new proxy' % callback)
                else:
                    old_count = Proxy.count()


if __name__ == '__main__':
    getter = Getter()
    getter.run()
