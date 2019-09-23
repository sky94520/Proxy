import os
import datetime
import logging


basedir = os.path.abspath(os.path.dirname(__file__))


# 日志格式化输出
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# 日期格式
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
NAME_FORMAT = "%H-%M-%S"

now = datetime.datetime.now()
filepath = os.path.join(basedir, 'files', 'log', now.strftime("%Y-%m-%d"))
if not os.path.exists(filepath):
    os.makedirs(filepath)
# 仅仅把警告以上的写入日志文件
filename = os.path.join(filepath, "%s.txt" % now.strftime("%H-%M-%S"))
fp = logging.FileHandler(filename, "w", encoding="utf-8")
fp.setLevel(logging.WARNING)

# 日志信息全部输出到控制台
fs = logging.StreamHandler()
fs.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])
