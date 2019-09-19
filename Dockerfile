FROM python:3.7

VOLUME ['/code']
WORKDIR /code

COPY requirements.txt /code

RUN pip install -r requirements.txt

# 暴露端口
EXPOSE 5555
# 脚本启动两个进程
CMD bash multiple_process.sh
