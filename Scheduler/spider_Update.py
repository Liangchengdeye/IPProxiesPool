#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: spider_Update.py 
@time: 2019/1/21 15:55 
@describe: 爬虫周期更新---未启用
1. 多线程周期更新
2. 分布式周期更新
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from BaseFile.ReadConfig import ReadConfig
SPIDERCONFIG = ReadConfig().get_conf("../Config/PROXYCONFIG.yaml")["spiderConfig"]


def spider_update():
    #爬虫周期更新
    xici = SPIDERCONFIG['xici']
    wuyou = SPIDERCONFIG['wuyou']
    if xici['ifRun'] is True:  # 是否运行
        print(xici)
    if wuyou['ifRun'] is True:
        print(wuyou)


def host_update():
    # 调度周期更新
    pass


if __name__ == '__main__':
    spider_update()




