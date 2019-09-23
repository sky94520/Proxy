#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

import asyncio
import aiohttp
from db import RedisClient
from asyncio import TimeoutError
from aiohttp.client_exceptions import ClientError, ClientConnectorError
import time
from api import STOP_TESTER_KEY
from config import BATCH_TEST_SIZE, VALID_STATUS_CODES, TEST_URL


class Tester(object):
    """
    测试类，会根据提供的测试IP地址来判断代理是否可用
    """
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        @param proxy: 单个代理
        return None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy

                print('Testing', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('Proxy useful', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('Response code invalid', proxy)
            except (ClientError, ClientConnectorError, TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('Proxy request error', proxy)

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
                # 外界正在使用代理池，则不再测试
                if self.redis.exist(STOP_TESTER_KEY):
                    break
                test_proxies = proxies[i: i + BATCH_TEST_SIZE]

                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]

                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('Tester errors', e.args)


if __name__ == '__main__':
    tester = Tester()
    tester.run()
