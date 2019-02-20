#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: ProxiesSpiderRun.py 
@time: 2019/2/20 10:01 
@describe: 运行代理爬虫
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from Spider.timerStartDaily import spider_run

if __name__ == '__main__':
    spider_run()