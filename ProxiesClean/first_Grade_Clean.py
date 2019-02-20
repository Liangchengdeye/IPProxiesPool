#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: first_Grade_Clean.py
@time: 2019/1/18 10:28 
@describe: 代理IP，初次验证处理-多进程调用
"""
import json
import random
import sys
import os
import time
from multiprocessing import Pool
import multiprocessing

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from BaseFile.ReadConfig import ReadConfig
from Common.RedisHelperLongConncet import RedisHelperConnect
from ProxiesTest.web_IP_Test import WebIpTest

CHECKOUTCONFIG = ReadConfig().get_conf("../Config/PROXYCONFIG.yaml")["checkoutConfig"]
BASEKEY = CHECKOUTCONFIG["redisBaseKeyName"]
GRADEKEY = CHECKOUTCONFIG["proxiesinitialGrade"]
GRADEKEY10 = CHECKOUTCONFIG["proxiesGrade10"]
GRADEKEY8 = CHECKOUTCONFIG["proxiesGrade8"]
GRADEKEY6 = CHECKOUTCONFIG["proxiesGrade6"]
GRADEKEY4 = CHECKOUTCONFIG["proxiesGrade4"]
# redis_pool = RedisHelper('proxiesRedis')
redis_pool = RedisHelperConnect()


# 代理IP初次评分
class GradeClan:
    def __init__(self, ip, port, anonymity, iptype, country, area, source):
        """
        代理IP处理
        :param ip:          代理IP
        :param port:        代理端口
        :param anonymity:   代理类型，普通，普匿，高匿
        :param iptype:      代理类型，HTTP,HTTPS
        :param country:     国家
        :param area:        地域
        :param source:      来源
        :      grade:       首次检验综合评分
        """
        self.ip = ip
        self.port = port
        self.anonymity = anonymity
        self.iptype = iptype
        self.country = country
        self.area = area
        self.source = source
        self.city = ["长城", "中国", "山东", "江苏", "上海", "浙江", "安徽", "福建", "江西", "广东", "广西", "海南", "河南", "湖南", "湖北", "北京",
                     "天津", "河北", "山西", "内蒙古", "宁夏", "青海", "陕西", "甘肃", "新疆", "四川", "贵州", "云南", "重庆", "西藏", "辽宁", "吉林",
                     "黑龙江", "香港", "澳门", "台湾"]

    def __get_ip(self):
        return self.ip.replace("\n", "").strip()

    def __get_port(self):
        return self.port.replace("\n", "").strip()

    def __get_anonymity(self):
        return self.anonymity.replace("\n", "").strip()

    def __get_iptype(self):
        return self.iptype.replace("\n", "").strip().upper()

    def __get_country(self):
        """
        国家分类
        :return: 中国 or 国外
        """
        country = self.country.replace("\n", "").strip()
        list_country = []
        [list_country.append("中国") for x in self.city if x in country]
        if len(list_country) < 1:
            list_country.append(country)
        return list_country[0]

    def __get_area(self):
        """
        国内省市分类
        :return:
        """
        area = self.area.replace("\n", "").replace("X", "").replace("*", "").replace("#", "").strip()
        list_str_area = []
        list_temp = []
        # 去重: 曼谷曼谷->曼谷
        [list_str_area.append(x) for x in area]
        [list_temp.append(y) for y in list_str_area if y not in list_temp]
        str_area = ""
        for g in list_temp:
            str_area += g
        list_area = []
        [list_area.append(z) for z in self.city if z in str_area]
        if len(list_area) < 1:
            list_area.append(str_area)
        return list_area[0]

    def __get_source(self):
        return self.source.replace("\n", "").strip()

    def __get_grade(self):
        return WebIpTest().return_grade(self.ip + ":" + self.port)

    def return_proxies(self):
        """
        :return: IP,HOST,匿名度,IP类型,国家,地区,来源,评分,评分时间
        """
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        grade = self.__get_grade()
        if grade != '999':
            return [self.__get_ip(), self.__get_port(), self.__get_anonymity(), self.__get_iptype(),
                    self.__get_country(),
                    self.__get_area(), self.__get_source(), grade, localtime]


number = 0


# 代理IP初次评分验证-从原始表获取IP并验证，按评分高低存入不同表，不同表内部自己轮询验证
class AutoGradeClean:

    @staticmethod
    def auto_grade_run(i, redis_base_key, redis_grade_key, redis_grade_key_10, redis_grade_key_8, redis_grade_key_6,
                       redis_grade_key_4, is_auto):
        """
        代理IP循环评分检验
        :param i:
        :param redis_base_key: 原始key
        :param redis_grade_key: 使用过后待检测key
        :param redis_grade_key_10: 评分为10的key
        :param redis_grade_key_8:       8
        :param redis_grade_key_6:       6
        :param redis_grade_key_4:       4-2
        :param is_auto: 队列顺序，True：前出前入，False：前出后入
        :return:
        """
        global number
        while True:
            number += 1
            print("number==============================================================>", number)
            ip_msg = str(redis_pool.redis_lpop(redis_base_key))
            # ip_msg = str(RedisHelperConnect().redis_lpop(CHECKOUTCONFIG["redisBaseKeyName"]))
            if len(ip_msg) == 0 or ip_msg == 'None' or ip_msg is None:
                print(i, "redis集合长度为空", random.randint(0, 10))
                time.sleep(1)
            else:
                print("1===>", ip_msg)
                ip_msg = json.loads(ip_msg.replace("'", "\""))
                area = ip_msg['area']
                if area == "" or len(area) == 0:
                    area = ip_msg['country']
                msg = GradeClan(ip_msg['ip'], ip_msg['port'], ip_msg['anonymity'], ip_msg['type'], ip_msg['country'],
                                area, ip_msg['source']).return_proxies()
                if msg is not None:
                    print("2===>", msg)
                    ip, port, anonymity, iptype, country, area, source, grade, searchtime = msg
                    proies_ok = json.dumps(
                        {"ip": ip, "port": port, "anonymity": anonymity, "type": iptype, "country": country,
                         "area": area, "source": source, "grade": grade, "searchtime": searchtime}, ensure_ascii=False)
                    print("result==>", proies_ok)
                    if is_auto is True:
                        if grade == '10':
                            redis_pool.redis_lpush(redis_grade_key_10, proies_ok)
                        if grade == '8':
                            redis_pool.redis_lpush(redis_grade_key_8, proies_ok)
                        if grade == '6':
                            redis_pool.redis_lpush(redis_grade_key_6, proies_ok)
                        if int(grade) <= 4:
                            redis_pool.redis_lpush(redis_grade_key_4, proies_ok)
                    else:
                        if grade == '10':
                            redis_pool.redis_rpush(redis_grade_key_10, proies_ok)
                        if grade == '8':
                            redis_pool.redis_rpush(redis_grade_key_8, proies_ok)
                        if grade == '6':
                            redis_pool.redis_rpush(redis_grade_key_6, proies_ok)
                        if int(grade) <= 4:
                            redis_pool.redis_rpush(redis_grade_key_4, proies_ok)


def first_clean_run(thread_number):
    """
    :param thread_number: 开启的进程数
    :return:
    """
    while True:
        print("start")
        pool = Pool(thread_number)
        for i in range(thread_number):
            msg = "hello %d" % (i)
            # 从原始表获取IP
            pool.apply_async(AutoGradeClean().auto_grade_run,
                             args=(msg, BASEKEY, GRADEKEY, GRADEKEY10, GRADEKEY8, GRADEKEY6, GRADEKEY4, False))
        pool.close()
        pool.join()


def first_grade_clean_run(thread_number, key_start):
    """
    评分IP池内周期自检
    :param thread_number: 开启进程数
    :param key_start: 10：开启评分为 10的代理 IP 池检验
    :param key_start: 8：开启评分为 8 的代理 IP 池检验
    :param key_start: 6：开启评分为 6 的代理 IP 池检验
    :param key_start: 4：开启评分为 4 的代理 IP 池检验
    :param key_start: 0：开启提供出去的 IP 活性代理 IP 池检验
    :return:
    """
    while True:
        print("start-grade")
        # pool = Pool(thread_number)
        pool = multiprocessing.Pool(processes=thread_number)
        # for i in range(thread_number*5):
        msg = "hello %d" % random.randint(1, 10)
        # # 从原始表获取IP
        # pool.apply_async(AutoGradeClean().auto_grade_run,
        #                  args=(msg, BASEKEY, GRADEKEY, GRADEKEY10, GRADEKEY8, GRADEKEY6, GRADEKEY4, False))
        autoGrade = AutoGradeClean()
        for i in range(thread_number):
            print(key_start)
            if key_start == '10':
                pool.apply_async(autoGrade.auto_grade_run,
                                 args=(10, GRADEKEY10, GRADEKEY, GRADEKEY10, GRADEKEY8, GRADEKEY6, GRADEKEY4, False))
            if key_start == '8':
                pool.apply_async(autoGrade.auto_grade_run,
                                 args=(8, GRADEKEY8, GRADEKEY, GRADEKEY10, GRADEKEY8, GRADEKEY6, GRADEKEY4, False))
            if key_start == '6':
                pool.apply_async(autoGrade.auto_grade_run,
                                 args=(6, GRADEKEY6, GRADEKEY, GRADEKEY10, GRADEKEY8, GRADEKEY6, GRADEKEY4, False))
            if key_start == '4':
                pool.apply_async(autoGrade.auto_grade_run,
                                 args=(4, GRADEKEY4, GRADEKEY, GRADEKEY10, GRADEKEY8, GRADEKEY6, GRADEKEY4, False))
            if key_start == '0':
                pool.apply_async(autoGrade.auto_grade_run,
                                 args=(0, GRADEKEY, GRADEKEY, GRADEKEY10, GRADEKEY8, GRADEKEY6, GRADEKEY4, True))

        pool.close()
        pool.join()


if __name__ == '__main__':
    first_clean_run(16)
