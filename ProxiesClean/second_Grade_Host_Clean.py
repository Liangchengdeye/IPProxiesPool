#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: second_Grade_Host_Clean.py 
@time: 2019/1/21 13:57 
@describe: 二次根据使用方传入的host或url，二次验证评分---未启用
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from Common.MySqlHelper import MysqlHelper
from ProxiesTest.target_IP_Test import TargetIpTest


class HostClean:
    def __init__(self, DBNAME):
        self.db = MysqlHelper(DBNAME)

    def __get_grade(self, url, ip):
        return TargetIpTest().target_grade(url, ip)

    def __get_ip(self, url):
        sql = '''SELECT * FROM proxiesinitial;'''
        list_ip = self.db.select(sql)
        list_host_grade = []
        for j in list_ip:
            first_grade = j[8]  # 首次评分
            host_name, second_grade = self.__get_grade(url, j[0]+":"+j[1])
            if second_grade != "999":
                grade = int(first_grade)+int(second_grade)
                j[8] = grade
                j.append(host_name)
                list_host_grade.append(j)
        return list_host_grade

    def return_proxies(self):
        print(self.__get_ip("http://www.baidu.com"))
        pass


if __name__ == '__main__':
    HostClean("test01").return_proxies()