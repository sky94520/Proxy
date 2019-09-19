#!/bin/bash

# 守护进程运行flask项目
echo 'start flask'
gunicorn --workers=4 --bind=0.0.0.0:5555 -d api:app

# 运行调度进程
python run.py