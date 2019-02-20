#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: ProxiesRun.py 
@time: 2019/2/15 17:18 
@describe: 运行代理池自检--默认开启8个进程
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from ProxiesClean.first_Grade_Clean import first_grade_clean_run


def run(key_start):
    """
    运行代理池自检
    :param key_start: 开启哪个自检池进程
    :return:
    """
    first_grade_clean_run(8, key_start)


if __name__ == '__main__':
    print("You can input (10,8,6,4,0)\n"
          "'10' is open grade of 10 ip pool check!\n"
          "'8' is open grade of 8 ip pool check!\n"
          "'6' is open grade of 6 ip pool check!\n"
          "'4' is open grade of 4/2 ip pool check!\n"
          "'0' is open is used ip pool check!")
    key_start = input("input start Thread Number(10,8,6,4,0):")
    run(key_start)