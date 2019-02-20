#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: target_IP_Test.py 
@time: 2019/1/17 18:42 
@describe: 目标网站测试类，对所要抓取的网站，使用代理IP验证一次，成功则进入目标网站代理池，否则抛弃
"""
import sys
import os
import requests
import re
from datetime import datetime
from requests.adapters import HTTPAdapter

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from Config.HEADERS import HEADERS as HS
from BaseFile.ReadConfig import ReadConfig

s = requests.Session()
# 超时读取配置文件
TIMEOUT = ReadConfig().get_conf("../Config/PROXYCONFIG.yaml")["webTestTimeOut"]["targetTimeOut"]
HOST_R = r'''(?xi)\A[a-z][a-z0-9+\-.]*://([a-z0-9\-._~%!$&'()*+,;=]+@)?([a-z0-9\-._~%]+|\[[a-z0-9\-._~%!$&'()*+,;=:]+\])'''
# 超时重试次数2次
s.mount('http://', HTTPAdapter(max_retries=2))
s.mount('https://', HTTPAdapter(max_retries=2))


def target_ip_second_test(hostUrl, IP):
    """
    目标网站响应时间测试方法
    :param hostUrl: 目标网站链接
    :param IP: 代理iP
    :return: 异常返回：('hostTest', 999, 999)
    """
    proxies = {"http": "http://{}".format(IP), "https": "http://{}".format(IP)}
    try:
        host = re.search(HOST_R, hostUrl, re.I | re.S).groups()[1]
    except:
        host = ""
    HS["hostUrlTest"]["Host"] = host
    try:
        start_time = datetime.now()
        html = s.get(hostUrl, proxies=proxies, timeout=TIMEOUT, headers=HS["hostUrlTest"], allow_redirects=False)
        status = html.status_code
        end_time = datetime.now()
        return host[host.find(".")+1:host.rfind(".")], status, (end_time - start_time).total_seconds()
    except Exception as e:
        return host[host.find(".")+1:host.rfind(".")], 999, 999


class TargetIpTest:

    @staticmethod
    def target_grade(url: str, IP: str):
        host_test = target_ip_second_test(url, IP)
        print(host_test)
        if host_test[1] != 200:
            return host_test[0], "999"
        else:
            h = host_test[2]
            if h <= 2:
                return host_test[0], "10"
            elif 2 < h <= 4:
                return host_test[0], "8"
            elif 4 < h <= 6:
                return host_test[0], "6"
            elif 6 < h <= 8:
                return host_test[0], "4"
            elif 8 < h <= 10:
                return host_test[0], "2"


if __name__ == '__main__':
    '''
    proxiesinitial: ip,port,anonymity,type,country,area,source,searchtime
    proxiesinitialgrade: ip,port,anonymity,type,country,area,source,grade,flag,searchtime
    '''
    # target = TargetIpTest().target_grade("http://httpbin.org/get?show_env=1", "111.26.9.26:80")
    target = TargetIpTest().target_grade("https://www.zhihu.com/question/47419361?sort=created", "23.253.54.249:3128")
    print(target)