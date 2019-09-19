#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

from multiprocessing import Process
from getter import Getter
from tester import Tester
import time
from config import TESTER_CYCLE, GETTER_CYCLE, TESTER_ENABLED, GETTER_ENABLED


class Scheduler(object):
    """
    调度类，会根据配置文件来选择是否开启对应的调度器
    """
    def schedule_tester(self, cycle=TESTER_CYCLE):
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

    def run(self):
        print('Proxy Pool start running')

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()


if __name__ == '__main__':
    scheduler = Scheduler()

    scheduler.run()
