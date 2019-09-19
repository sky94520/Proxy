#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

from db import RedisClient
from crawler import Crawler
from config import POOL_UPPER_THRESHOLD


class Getter(object):
    """
    根据阈值判断是否爬取
    """
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        return self.redis.count() >= POOL_UPPER_THRESHOLD

    def run(self):
        print('Getter now running')

        if not self.is_over_threshold():
            for callback in self.crawler.__CrawlFunc__:
                proxies = self.crawler.get_proxies(callback)

                for proxy in proxies:
                    self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()

    getter.run()
