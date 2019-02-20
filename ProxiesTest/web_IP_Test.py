#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: web_IP_Test.py
@time: 2019/1/17 17:28 
@describe: 代理IP是否可用测试，通过百度和telnet进行验证并评分；
响应时间：
    0-1s:  10 分
    1-2s:  8 分
    2-3s:  6 分
    3-4s:  4 分
    4-5s: 2 分
    未知：999分
访问 http://www.baidu.com
https://www.baidu.com
"""
import sys
import os
import telnetlib
from datetime import datetime
import requests
import time
import threading

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from Config.HEADERS import HEADERS as HS
from BaseFile.ReadConfig import ReadConfig as RC

# 超时读取配置文件
TIMEOUT = RC().get_conf("../Config/PROXYCONFIG.yaml")["webTestTimeOut"]


class MyThread(threading.Thread):
    """
    多线程初始化
    """

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.name = name
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result


def get_baidu(IP):
    """
    测试百度响应时间
    :param IP:
    :return: 异常返回： ('baidu', 999, 999)
    """
    try:
        start_time = datetime.now()
        pro = {"http": "http://{}".format(IP)}
        time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        html = requests.get("http://www.baidu.com/", proxies=pro, timeout=TIMEOUT["baiduTimeOut"],
                            headers=HS["baiduTest"])
        end_time = datetime.now()
        diff = (end_time - start_time).total_seconds()
        return "baidu", html.status_code, diff
    except:
        return "baidu", 999, 999


def get_telnet(IP):
    """
    测试Telnet响应时间
    :param IP:
    :return: 异常响应：('telnet', 999, 999)
    """
    try:
        start_time = datetime.now()
        host, port = IP.split(":")
        telnetlib.Telnet(host=str(host), port=int(port), timeout=TIMEOUT["telnetTimeOut"])
        end_time = datetime.now()
        diff = (end_time - start_time).total_seconds()
        return "telnet", 200, diff
    except:
        return "telnet", 999, 999


def web_proxies_first_test(IP):
    """
    多线程测试百度和Telnet
    :param IP: 入参：111.26.9.26:80
    :return: [('telnet', 200, 0.029002), ('telnet', 200, 0.029002)]
    """
    funcs = [get_baidu, get_telnet]
    nfuncs = range(len(funcs))
    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (IP,), funcs[i].__name__)
        threads.append(t)

    for j in nfuncs:
        threads[j].start()
    list_result = []
    for k in nfuncs:
        threads[k].join()
        list_result.append(threads[k].get_result())
    return list_result


class WebIpTest:

    @staticmethod
    def return_grade(IP: str):
        """对检验过的IP进行评分
            0-1s:  10 分
            1-2s:  8 分
            2-3s:  6 分
            3-4s:  4 分
            4-5s: 2 分
            未知：999分
        """
        baidu, telnet = web_proxies_first_test(IP)
        # print(baidu, telnet)
        if baidu[1] != 200 or telnet[1] != 200:
            return '999'
        else:
            b = baidu[2]
            t = telnet[2]
            if b + t <= 2:
                return "10"
            elif 2 < b+t <= 4:
                return "8"
            elif 4 < b+t <= 6:
                return "6"
            elif 6 < b+t <= 8:
                return "4"
            elif 8 < b+t <= 10:
                return "2"


if __name__ == '__main__':
    IP = "110.52.235.32:9999"
    web = WebIpTest().return_grade(IP)
    print(web)