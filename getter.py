#! /usr/bin/python3.6
# -*-coding:utf-8 -*-
"""
负责调用爬虫
"""

from crawler import Crawler
from settings import POOL_UPPER_THRESHOLD
from db import RedisClient
import log
import logging


class Getter(object):
    """
    根据阈值判断是否爬取
    """
    def __init__(self):
        self.crawler = Crawler()
        self.redis = RedisClient()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        return self.redis.count() >= POOL_UPPER_THRESHOLD

    def run(self):
        if not self.is_over_threshold():
            logging.info('Getter now running')
            old_count = self.redis.count()
            # 调用爬虫方法
            for callback in self.crawler.__CrawlFunc__:
                # 爬取数据
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
                new_count = self.redis.count()
                # 未爬取到数据
                if old_count == new_count and len(proxies) == 0:
                    logging.error('%s function can\'t crawl new proxy' % callback)
                elif old_count != new_count:
                    logging.info('%s crawl %d proxies' % (callback, (new_count - old_count)))
                    old_count = new_count


if __name__ == '__main__':
    getter = Getter()
    getter.run()
