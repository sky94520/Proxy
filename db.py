#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

import redis
from redis.exceptions import DataError
from random import choice
from config import MAX_SCORE, MIN_SCORE, INITIAL_SCORE, REDIS_KEY, REDIS_CONFIG


class RedisClient(object):
    def __init__(self):
        """初始化"""
        self.db = redis.StrictRedis(**REDIS_CONFIG, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，分数为初始分数
        @param proxy: 代理
        @param score: 分数
        @return: 添加结果
        """
        # 不存在该代理键值对，则添加
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
        随机获取有效代理，首先随机获取分值最高的代理，如果不存在，则按照排名获取，否则异常
        @return 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise DataError

    def decrease(self, proxy):
        """
        代理值减一，分值小于最小值时则删除
        @param proxy: 代理
        return 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)

        if score and score > MIN_SCORE:
            print('Proxy', proxy, 'Current score', score, 'sub 1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('Proxy', proxy, 'Current score', score, 'removed')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        @param proxy: 代理
        return 是否存在
        """
        return self.db.zscore(REDIS_KEY, proxy) is not None

    def max(self, proxy):
        """
        将代理设置为最大值MAX_SCORE
        """
        print('Proxy', proxy, 'is Useful,and the score set to', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取数量
        return 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部递增代理
        return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
