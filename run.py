#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

from multiprocessing import Process
from api import app
from getter import Getter
from tester import Tester
import time

# 每若干秒为一个循环
TESTER_CYCLE = 20
GETTER_CYCLE = 20
# 是否开启对应的调度器
TESTER_ENABLED = True
GETTER_ENABLED = False
API_ENABLED = True
# 面向的API
API_HOST = '0.0.0.0'
API_PORT = 5555


class Scheduler(object):
    """
    调度类，会根据配置文件来选择是否开启对应的调度器
    """
    def schedule_tester(self, cycle=GETTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()

        while True:
            print('Tester start running')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()

        while True:
            print('Start crawling proxy')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启api
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('Proxy Pool start running')

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()


if __name__ == '__main__':
    scheduler = Scheduler()

    scheduler.run()
