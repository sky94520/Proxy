"""
使用了SQLAlchemy向外提供数据
"""
import logging
import random
import pymysql
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from settings import INITIAL_SCORE, MAX_SCORE, MIN_SCORE
from config import SQL_ALCHEMY_URI

engine = create_engine(SQL_ALCHEMY_URI, pool_size=10)
Base = declarative_base()


class Proxy(Base):
    __tablename__ = 'proxy'
    ip = Column(String(32), primary_key=True)
    port = Column(Integer, primary_key=True)
    score = Column(Integer)

    @staticmethod
    def count():
        count = session.query(Proxy).count()
        return count

    @staticmethod
    def add_one(proxy, score=INITIAL_SCORE):
        """
        添加代理数组，分数为初始分数
        @param proxy: 代理
        @param score: 分数
        @return: 添加结果
        """
        try:
            proxy.score = score
            session.add(proxy)
            session.commit()
        except IntegrityError as e:
            session.rollback()

    @staticmethod
    def add(proxies, score=INITIAL_SCORE):
        """
        添加代理数组，分数为初始分数
        @param proxies: 代理
        @param score: 分数
        @return: 添加结果
        """
        # 把代理拆分成ip port
        for proxy in proxies:
            proxy.score = score
        try:
            # 批量添加
            session.add_all(proxies)
            session.commit()
        except Exception as e:
            logging.error(e)
            session.rollback()

    @staticmethod
    def random():
        """
        随机获取有效代理，首先随机获取分值最高的代理，如果不存在，则按照排名获取，否则异常
        @return 随机代理
        """
        results = session.query(Proxy).filter(Proxy.score >= MAX_SCORE).all()
        if len(results) == 0:
            return None
        proxy = random.choice(results)
        return proxy

    def decrease(self, delta=-1):
        """
        代理值减一，分值小于最小值时则删除
        :param delta: 要减去的分数值
        return 修改后的代理分数
        """
        self.score = min(max(MIN_SCORE, self.score + delta), MAX_SCORE)
        session.add(self)
        session.commit()
        return self.score

    def max(self):
        """
        将代理设置为最大值MAX_SCORE
        """
        self.score = MAX_SCORE
        session.add(self)
        session.commit()

    @staticmethod
    def all():
        """
        获取全部递增代理
        :return:
        """
        results = session.query(Proxy).order_by(Proxy.score).all()
        return results

    def __str__(self):
        return '%s:%d' % (self.ip, self.port)

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port

    def __hash__(self):
        return hash((self.ip, self.port))


Base.metadata.bind = engine
Base.metadata.create_all()


Session = sessionmaker(bind=engine)
session = Session()


if __name__ == '__main__':
    print(Proxy.random())
