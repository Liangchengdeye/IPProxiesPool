#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: apiTest.py 
@time: 2019/2/14 16:58 
@describe: API 测试
"""
import sys
import os

import requests

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


def get_status():
    html = requests.get("http://127.0.0.1:8020/proxies/status")
    print(html.text)


def get_proxies():
    html = requests.get("http://127.0.0.1:8020/proxies/get")
    print(html.text)


def get_proxies_ip():
    html = requests.get("http://127.0.0.1:8020/proxies/getip")
    print(html.text)


if __name__ == '__main__':
    # 查看状态
    # get_status()

    # 获取一个可用IP
    # get_proxies()

    # 获取一个代理
    print(get_proxies_ip())
