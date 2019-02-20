#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: proxies_Update.py 
@time: 2019/2/15 15:59 
@describe: ip使用调度；
提供策略：
评分高低依据：响应时长
评分:10->8->6->4
一次从评分最高到最低，在相应的检测过的IP池内提供一个可用IP；同时将该IP插入到待检验池，重新
轮询验证该IP可用性，并对其评分；
"""
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from BaseFile.ReadConfig import ReadConfig
from Common.RedisHelperLongConncet import RedisHelperConnect

CHECKOUTCONFIG = ReadConfig().get_conf("../Config/PROXYCONFIG.yaml")["checkoutConfig"]
BASEKEY = CHECKOUTCONFIG["redisBaseKeyName"]
GRADEKEY = CHECKOUTCONFIG["proxiesinitialGrade"]
GRADEKEY10 = CHECKOUTCONFIG["proxiesGrade10"]
GRADEKEY8 = CHECKOUTCONFIG["proxiesGrade8"]
GRADEKEY6 = CHECKOUTCONFIG["proxiesGrade6"]
GRADEKEY4 = CHECKOUTCONFIG["proxiesGrade4"]
redis_pool = RedisHelperConnect()


def proxies_get(gradekey10, gradekey8, gradekey6, gradekey4):
    """
    返回一个代理IP
    :param gradekey10: 评分 10
    :param gradekey8:       8
    :param gradekey6:       6
    :param gradekey4:       4-2
    :return: IP
    """
    try:
        len_grade_10 = redis_pool.redis_llen(gradekey10)
        if len_grade_10 > 0:  # 提供一个IP出去，同时将该IP从左侧加入到待检测队列，重新评分--越好越用，贪婪使用
            proxies_10 = redis_pool.redis_lpop(gradekey10)
            redis_pool.redis_lpush(GRADEKEY, proxies_10)
            return proxies_10
        else:
            len_grade_8 = redis_pool.redis_llen(gradekey8)
            if len_grade_8 > 0:
                proxies_8 = redis_pool.redis_lpop(gradekey8)
                redis_pool.redis_lpush(GRADEKEY, proxies_8)
                return proxies_8
            else:
                len_grade_6 = redis_pool.redis_llen(gradekey6)
                if len_grade_6 > 0:
                    proxies_6 = redis_pool.redis_lpop(gradekey6)
                    redis_pool.redis_lpush(GRADEKEY, proxies_6)
                    return proxies_6
                else:
                    len_grade_4 = redis_pool.redis_llen(gradekey4)
                    if len_grade_4 > 0:
                        proxies_4 = redis_pool.redis_lpop(gradekey4)
                        redis_pool.redis_lpush(GRADEKEY, proxies_4)
                        return proxies_4
                    else:
                        return json.dumps({"IP": "NULL"})
    except Exception as e:
        print(e)
        return json.loads({"IP": "NULL"})


def proxies_Update_main():
    return proxies_get(GRADEKEY10, GRADEKEY8, GRADEKEY6, GRADEKEY4)


def proxies_get_number():
    """
    获取代理IP数量
    :return:
    """
    number_10 = redis_pool.redis_llen(GRADEKEY10)
    number_8 = redis_pool.redis_llen(GRADEKEY8)
    number_6 = redis_pool.redis_llen(GRADEKEY6)
    number_4 = redis_pool.redis_llen(GRADEKEY4)
    number_grade = redis_pool.redis_llen(GRADEKEY)  # 使用完待检测IP条数
    number_base = redis_pool.redis_llen(BASEKEY)  # 原始IP条数
    return number_10, number_8, number_6, number_4, number_grade, number_base


if __name__ == '__main__':
    # print(proxies_Update_main())
    print(proxies_get_number())
