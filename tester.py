#! /usr/bin/python3.6
# -*-coding:utf-8 -*-
"""
测试
"""

import logging
import asyncio
import aiohttp
from asyncio import TimeoutError
from aiohttp.client_exceptions import ClientError, ClientConnectorError
import time
from settings import BATCH_TEST_SIZE, VALID_STATUS_CODES, TEST_URL
from db import RedisClient


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()
    """
    测试类，会根据提供的测试IP地址来判断代理是否可用
    """
    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        @param proxy: 单个代理
        return None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                real_proxy = 'http://%s' % proxy
                async with session.get(TEST_URL, proxy=real_proxy, timeout=2) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                    else:
                        self.redis.decrease(proxy)
            except (ClientError, ClientConnectorError, TimeoutError, AttributeError):
                self.redis.decrease(proxy)

    def run(self):
        """
        测试主函数
        """
        print('Starting test')
        try:
            # 获取所有的代理
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            # 批量测试
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i: i + BATCH_TEST_SIZE]

                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]

                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('Tester errors', e.args)


if __name__ == '__main__':
    tester = Tester()
    tester.run()
