#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: ProxiesCheckRun.py 
@time: 2019/2/19 19:31 
@describe: 启动代理IP检验，开启16个进程
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from ProxiesClean.first_Grade_Clean import first_clean_run


def run():
    first_clean_run(16)


if __name__ == '__main__':
    print("===> 开启代理IP循环检验，进程数量：16")
    run()
