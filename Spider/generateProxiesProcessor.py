#!/usr/bin/env python  
# encoding: utf-8  
""" 
@author: jingjingli 
@software: PyCharm
@file: generateProxiesProcessor.py
@time: 2019/1/21
@describe: proxypool --代理IP抓取

"""
import os
import sys
from pyquery import PyQuery
import requests
import json
import time
import re
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from BaseFile.ReadConfig import ReadConfig
from Common.RedisHelperLongConncet import RedisHelperConnect
from Config.HEADERS import HEADERS
from Common.MySqlHelper import MysqlHelper

SUM = 0
CHECKOUTCONFIG = ReadConfig().get_conf("../Config/PROXYCONFIG.yaml")["spiderConfig"]
# 获取一个代理，防止网站反爬
PROXIESIP = CHECKOUTCONFIG["proxiesIP"]['proxies']


# 公共爬虫方法
def spider_common(url, headers, timeout, encoding):
    # 设置超时时间为5
    try:
        html = requests.get(url, headers=headers, timeout=timeout)
        html.encoding = encoding
        html_headers = html.headers
        html_text = html.text
        print("0 == html code ==>", html.status_code)
        print("1 == html headers ==>", html_headers)
        print("2 == html url ==>", url)
        return html_text
    except Exception as e:
        print("SPIDER COMMON:", e)


# 通过代理抓取代理类，
def spider_common_ip(proxiesIP, url, headers, timeout, encoding):
    # 设置超时时间为5
    try:
        # html = requests.get("http://123.207.35.36:5010/get/")
        html = requests.get(proxiesIP)
        proxies = {"http": "http://%s" % html.text}
        html = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
        html.encoding = encoding
        html_headers = html.headers
        html_text = html.text

        print("0 == html code ==>", html.status_code)
        print("1 == html headers ==>", html_headers)
        print("2 == html url ==>", url)
        return html_text
    except Exception as e:
        global NETWORK_STATUS
        # 请求超时改变状态
        NETWORK_STATUS = False
        if NETWORK_STATUS == False:
            for i in range(1, 10):  # 超时重试
                try:
                    # html = requests.get("http://123.207.35.36:5010/get/")
                    html = requests.get(proxiesIP)
                    proxies = {"http": "http://%s" % html.text}
                    print('请求超时，第 % s次重复请求' % i, proxies)
                    html = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
                    if html.status_code == 200:
                        html_headers = html.headers
                        html_text = html.text
                        print("0 == html code ==>", html.status_code)
                        print("1 == html headers ==>", html_headers)
                        print("2 == html url ==>", url)
                        return html_text
                    else:
                        print("********************", html.text)
                    NETWORK_STATUS = True
                except:
                    print("*************")
        return -1


def get_qydaili_html(url):
    try:
        html_text = spider_common(url, HEADERS["qydaili"], 5, 'utf-8')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_qydaili_html(url)
            else:
                return
        doc = PyQuery(html_text)
        trs = doc("table.table.table-bordered.table-striped > tbody > tr").items()
        ipInfo_list = []
        for i in trs:
            td = i.text()
            tdlist = td.split('\n')
            ip = tdlist[0]
            port = tdlist[1]
            anonymity = tdlist[2]
            if anonymity == "高匿":
                anonymity = "2"
            elif anonymity == "匿名":
                anonymity = "1"
            else:
                anonymity = "0"
            iptype = tdlist[3]
            if "unchina" in url:
                country = tdlist[4].split(" ", 1)[0]
                area = tdlist[4].split(" ", 1)[1]
            else:
                country = "中国"
                area = tdlist[4].replace("中国", "").strip()
            source = "qydaili"

            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (str(ip), str(port), str(anonymity), str(iptype), country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_xicidaili_html(url):
    try:
        html_text = spider_common(url, HEADERS["xicidaili"], 5, 'utf-8')
        print(html_text)
        doc = PyQuery(html_text)
        trs = doc("table#ip_list > tr").items()
        ipInfo_list = []
        for i in trs:
            td = i("td").text()
            if len(td) != 0:
                tdlist = i("td").text().split(" ")
                # print(tdlist)
                ip = tdlist[1]
                port = tdlist[2]
                anonymity = tdlist[4]
                if anonymity == "高匿":
                    anonymity = "2"
                elif anonymity == "透明":
                    anonymity = "0"
                else:
                    anonymity = "1"
                iptype = tdlist[5]
                country = "中国"
                area = tdlist[3]
                source = "xicidaili"

                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_data5u_html(url):
    try:
        html_text = spider_common(url, HEADERS["data5u"], 5, 'utf-8')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_data5u_html(url)
            else:
                return
        doc = PyQuery(html_text)
        trs = doc("body > div:nth-child(7) > ul > li:nth-child(2) > ul.l2").items()
        ipInfo_list = []
        for i in trs:
            li_list = i.text().split("\n")
            ip = li_list[0]
            port = li_list[1]
            anonymity = li_list[2]
            if anonymity == "高匿":
                anonymity = "2"
            elif anonymity == "透明":
                anonymity = "0"
            else:
                anonymity = "1"
            iptype = li_list[3]
            country = li_list[4]
            area = li_list[5]
            source = "data5u"

            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_66ip_country_html(url):
    try:
        html_text = spider_common(url, HEADERS["66ip"], 5, 'gbk')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_66ip_country_html(url)
            else:
                return
        doc = PyQuery(html_text)
        trs = doc('body > div:nth-child(3) > table > tr > td > ul > li').items()
        for i in trs:
            li = i("a").attr("href")
            if "areaindex" in li:
                url = "http://www.66ip.cn" + li
                get_66ip_city_ipInfo(url)
            if "areaindex" not in li:
                url = "http://www.66ip.cn"
                get_66ip_abroad_ipInfo(url)
    except Exception as e:
        print("SPIDER COMMON:", e)


# 地方代理
def get_66ip_city_ipInfo(url):
    try:
        html_text = spider_common(url, HEADERS["66ip"], 5, 'gbk')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_66ip_city_ipInfo(url)
            else:
                return
        doc = PyQuery(html_text)
        trs = doc('#footer > div > table > tr').items()
        ipInfo_list = []
        for i in trs:
            td = i("td").text()
            if "端口号" not in td:
                td_list = td.split(" ")
                ip = td_list[0]
                port = td_list[1]
                anonymity = td_list[3]
                if anonymity == "高匿代理":
                    anonymity = "2"
                elif anonymity == "匿名":
                    anonymity = "1"
                else:
                    anonymity = "0"
                iptype = ""
                country = "中国"
                area = td_list[2]
                source = '66ip'

                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# 国外代理
def get_66ip_abroad_ipInfo(url):
    try:
        html_text = spider_common(url, HEADERS["66ip"], 5, 'gbk')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_66ip_abroad_ipInfo(url)
            else:
                return
        doc = PyQuery(html_text)
        trs = doc('#main > div > div:nth-child(1) > table > tr').items()
        ipInfo_list = []
        for i in trs:
            td = i("td").text()
            if "端口号" not in td:
                td_list = td.split(" ")
                ip = td_list[0]
                port = td_list[1]
                anonymity = td_list[3]
                if anonymity == "高匿代理":
                    anonymity = "2"
                elif anonymity == "匿名":
                    anonymity = "1"
                else:
                    anonymity = "0"
                iptype = ""
                country = "中国"
                area = td_list[2]
                source = '66ip'

                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_kuaidaili_html(url):
    try:
        html_text = spider_common(url, HEADERS["kuaidaili"], 5, 'utf-8')
        print(html_text)
        doc = PyQuery(html_text)
        trs = doc("#freelist > table > tbody > tr").items()
        ipInfo_list = []
        for i in trs:
            td = i("td").text().replace("中国", "").strip()
            if 'HTTP, HTTPS' in td:
                td = td.replace("HTTP, HTTPS", "HTTP")
            else:
                td = td
            td_list = td.split(" ")
            while '' in td_list:
                td_list.remove('')
            # print(td_list)
            ip = td_list[0]
            port = td_list[1]
            anonymity = td_list[2]
            if anonymity == "高匿名":
                anonymity = "2"
            elif anonymity == "匿名":
                anonymity = "1"
            else:
                anonymity = "0"
            iptype = td_list[3]
            country = "中国"
            area = td_list[6]
            source = "kuaidaili"
            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_goubanjia_html(url):
    try:
        html_text = spider_common_ip(url, HEADERS["goubanjia"], 10, 'utf-8')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_goubanjia_html(url)
            else:
                return
        doc = PyQuery(html_text)
        tds = doc("#services > div > div.row > div > div > div > table > tbody > tr > td.ip").items()
        trs = doc("#services > div > div.row > div > div > div > table > tbody > tr").items()
        ipInfo_list = []
        for i in trs:
            ip_str = str(i.html())
            re_style = re.compile('<\s*p[^>]*>[^<]*<\s*/\s*p\s*>', re.I)  # style
            s = re.sub(re_style, '', ip_str)  # 去掉style
            ip_doc = PyQuery(s).text()
            ip_list = ip_doc.replace("\n", "")
            td_list = ip_list.split(":")
            ip = td_list[0]
            td = i("td").text()
            if i("td").attr('class') == 'ip':
                td = td.replace("\n", "")
            else:
                td = td
            td_list = td.split()
            # ip = td_list[0].split(":")[0]
            port = td_list[0].split(":")[1]
            anonymity = td_list[1]
            if anonymity == "透明":
                anonymity = "0"
            elif anonymity == "匿名":
                anonymity = "1"
            else:
                anonymity = "2"
            iptype = td_list[2]
            country = td_list[3]
            area = td_list[4] + td_list[5]
            source = "quanwangdailiip"
            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_ip3366_html(url):
    try:
        html_text = spider_common_ip(PROXIESIP, url, HEADERS["ip3366"], 10, 'gbk')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text or "网站防火墙" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_ip3366_html(url)
            else:
                return
        doc = PyQuery(html_text)
        trs = doc('#list > table > tbody > tr').items()
        ipInfo_list = []
        for i in trs:
            ipInfoList = i('td').text().split(' ')
            ip = ipInfoList[0]
            port = ipInfoList[1]
            anonymity = ipInfoList[2]
            if anonymity == '透明代理IP':
                anonymity = '0'
            elif anonymity == '普通代理IP':
                anonymity = '1'
            else:
                anonymity = '2'
            iptype = ipInfoList[3]
            if 'stype=1' or 'stype=2' in url:
                country = '中国'
            elif '' or '' in url:
                country = ""

            area = ipInfoList[4].replace("高匿_", "").replace("SSL高匿_", "")
            source = 'ip3366'

            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), anonymity, iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_zdaye_html(url):
    try:
        html_text = spider_common_ip(PROXIESIP, url, HEADERS["zdaye"], 10, 'gb2312')
        print(html_text)
        doc = PyQuery(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_zdaye_html(url)
            else:
                return
        alis = doc(
            'body > div.container.mt40 > div.container.mt40 > div.col-md-3.admin_arrow_box > div:nth-child(1) > a:nth-child(2)').items()
        for i in alis:
            url = 'http://ip.zdaye.com' + i.attr('href')
            print(url)
            get_zdaye_ipUrl(url)
    except Exception as e:
        print("SPIDER COMMON:", e)


def get_zdaye_ipUrl(url):
    try:
        html_text = spider_common_ip(PROXIESIP, url, HEADERS["zdaye"], 10, 'gb2312')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_zdaye_ipUrl(url)
            else:
                return
        doc = PyQuery(html_text)
        a1 = doc(
            'body > div.container.mt40 > div.container.mt40 > div.col-md-9 > div > div > div.panel.panel-success > div.panel-body > div.row > div:nth-child(2) > div:nth-child(2) > div.title > a').attr(
            "href")
        a2 = doc(
            'body > div.container.mt40 > div.container.mt40 > div.col-md-9 > div > div > div.panel.panel-success > div.panel-body > div.row > div:nth-child(2) > div:nth-child(3) > div.title > a').attr(
            "href")
        url1 = "http://ip.zdaye.com" + str(a1)
        url2 = "http://ip.zdaye.com" + str(a2)
        get_zdaye_ipInfo(url1)
        get_zdaye_ipInfo(url2)
    except Exception as e:
        print("SPIDER COMMON:", e)


def get_zdaye_ipInfo(url):
    try:
        html_text = spider_common_ip(PROXIESIP, url, HEADERS["zdaye"], 5, 'gb2312')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_zdaye_ipInfo(url)
            else:
                return
        doc = PyQuery(html_text)
        brs = doc('div.col-md-9 > div > div > div > div.panel-body > div > div:nth-child(2) > div.cont').text()
        ipInfo_list = []
        iplist = brs.split("\n")
        for i in iplist:
            ip = i.split(':')[0]
            port = i.split(":")[1].split("@")[0]
            iptype = i.split(":")[1].split("@")[1].split("#")[0]
            area = i.split(":")[1].split("@")[1].split("#")[1].split("]")[1].split(' ')[0]
            anonymity = i.split(":")[1].split("@")[1].split("#")[1].split("]")[0].lstrip('[')
            if anonymity == '透明':
                anonymity = '0'
            elif anonymity == '高匿名':
                anonymity = '2'
            else:
                anonymity = '1'
            title = doc(
                'div.taglineWrap > div > div.col-md-9 > div > div > div > div.panel-body > div > div:nth-child(2) > div.title').text()
            if '国内' in title:
                country = '中国'
            else:
                country = area
                area = ''
            source = "zdaye"

            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_89ip_html(url):
    try:
        html_text = spider_common(url, HEADERS["89ip"], 5, 'utf-8')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_zdaye_ipInfo(url)
            else:
                return
        doc = PyQuery(html_text)
        tr = doc(
            'div.layui-row.layui-col-space15 > div.layui-col-md8 > div > div.layui-form > table > tbody > tr').items()
        ipInfo_list = []
        for i in tr:
            ipInfo = i('td').text().split(' ')
            ip = ipInfo[0]
            port = ipInfo[1]
            anonymity = ""
            iptype = ""
            country = "中国"
            area = ipInfo[2]
            source = "89ip"

            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************

def get_xsdaili_html(url):
    try:
        html_text = spider_common_ip(PROXIESIP, url, HEADERS["xsdaili"], 5, 'utf-8')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text or "function setCookie(name,value)" in html_text or "404 Not Found" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_zdaye_ipInfo(url)
            else:
                return
        doc = PyQuery(html_text)
        alis = doc('div.taglineWrap > div > div.col-md-3.admin_arrow_box > div > a:nth-child(2)').items()
        for i in alis:
            if i.attr('href') != '/':
                url = "http://www.xsdaili.com/" + i.attr('href')
                get_xsdaili_ipUrl(url)
    except Exception as e:
        print("SPIDER COMMON:", e)


def get_xsdaili_ipUrl(url):
    try:
        html_text = spider_common_ip(PROXIESIP, url, HEADERS["xsdaili"], 5, 'utf-8')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_zdaye_ipInfo(url)
            else:
                return
        doc = PyQuery(html_text)
        divs = doc(
            'div.taglineWrap > div > div.col-md-9 > div > div > div > div.panel-body > div > div:nth-child(2)').items()
        for i in divs:
            url1 = 'http://www.xsdaili.com' + i('div:nth-child(2) > div.cont > a').attr('href')
            url2 = 'http://www.xsdaili.com' + i('div:nth-child(3) > div.cont > a').attr('href')
            url3 = 'http://www.xsdaili.com' + i('div:nth-child(4) > div.cont > a').attr('href')
            url4 = 'http://www.xsdaili.com' + i('div:nth-child(5) > div.cont > a').attr('href')
            get_xsdaili_ipInfo(url1)
            get_xsdaili_ipInfo(url2)
            get_xsdaili_ipInfo(url3)
            get_xsdaili_ipInfo(url4)
    except Exception as e:
        print("SPIDER COMMON:", e)


def get_xsdaili_ipInfo(url):
    try:
        html_text = spider_common_ip(PROXIESIP, url, HEADERS["xsdaili"], 5, 'gbk')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_zdaye_ipInfo(url)
            else:
                return
        doc = PyQuery(html_text)
        brs = doc('div.col-md-9 > div > div > div > div.panel-body > div > div:nth-child(2) > div.cont').text()
        ipInfo_list = []
        iplist = brs.split("\n")
        for i in iplist:
            ip = i.split(':')[0]
            port = i.split(":")[1].split("@")[0]
            iptype = i.split(":")[1].split("@")[1].split("#")[0]
            area = i.split(":")[1].split("@")[1].split("#")[1].split("]")[1].split(' ')[0]
            anonymity = i.split(":")[1].split("@")[1].split("#")[1].split("]")[0].lstrip('[')
            if anonymity == '透明':
                anonymity = '0'
            elif anonymity == '高匿名':
                anonymity = '2'
            else:
                anonymity = '1'
            title = doc(
                'div.taglineWrap > div > div.col-md-9 > div > div > div > div.panel-body > div > div:nth-child(2) > div.title').text()
            if '国内' in title:
                country = '中国'
            else:
                country = area
                area = ''
            source = "xsdaili"
            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_31f_html(url):
    html_text = spider_common_ip(PROXIESIP, url, HEADERS["31f"], 10, 'utf-8')
    print(html_text)
    try:
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_31f_html(url)
            else:
                return
        doc = PyQuery(html_text)
        trs = doc("body > div > table.table.table-striped > tr").items()
        ipInfo_list = []
        for i in trs:
            td = i("td").text().strip()
            td_list = td.split(" ")
            while '' in td_list:
                td_list.remove('')
            if len(td_list) != 0:
                ip = td_list[1]
                port = td_list[2]
                anonymity = td_list[6]
                if anonymity == "transparent":
                    anonymity = "0"
                elif anonymity == "anonymous":
                    anonymity = "1"
                else:
                    anonymity = "2"
                iptype = ""
                country = "中国"
                area = td_list[3] + td_list[4]
                source = "31f"

                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_ab57_html(url):
    try:
        html_text = spider_common(url, HEADERS["ab57"], 5, 'utf-8')
        print(html_text)
        ipInfo = html_text.split("\n")
        ipInfo_list = []
        for i in ipInfo:
            if i != "" and len(i) != 0 and i != ":":
                ipAndPort = i.split(":")
                ip = ipAndPort[0]
                port = ipAndPort[1]
                anonymity = ""
                iptype = ""
                country = ""
                area = ""
                source = "ab57"

                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_atomintersoft_html(url):
    try:
        html_text = spider_common(url, HEADERS["atomintersoft"], 5, 'utf-8')
        doc = PyQuery(html_text)
        tr = doc('#node-20 > div.content.clear-block > fieldset:nth-child(2) > div > table > tbody > tr > td').items()
        for i in tr:
            url = "http://www.atomintersoft.com" + i("a").attr("href")
            print(url)
            get_atomintersoft_ipInfo(url)
    except Exception as e:
        print("SPIDER COMMON:", e)


def get_atomintersoft_ipInfo(url):
    try:
        html_text = spider_common(url, HEADERS["atomintersoft"], 5, 'utf-8')
        doc = PyQuery(html_text)
        tr = doc('div.node > div.content > fieldset.collapsible:eq(1) > div.form-item > table > thead > tr').items()
        ipInfo_list = []
        for i in tr:
            td = i('td:nth-child(1)').items()
            for j in td:
                ele = j.text().split('\n')
                ip = ele[0].split(":")[0]
                port = ele[0].split(":")[1]
                anonymity = ele[3]
                if anonymity == "Transparent":
                    anonymity = "0"
                elif anonymity == "High anonymity":
                    anonymity = "2"
                else:
                    anonymity = "1"
                iptype = ""
                country = ele[2]
                area = ""
                source = "atomintersoft"

                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_rmccurdy_html(url):
    try:
        html_text = spider_common(url, HEADERS["rmccurdy"], 5, 'utf-8')
        ipInfo = html_text.split("\n")
        ipInfo_list = []
        for i in ipInfo:
            if i != "" and len(i) != 0 and i != ":":
                ipAndPort = i.split(":")
                ip = ipAndPort[0]
                port = ipAndPort[1]
                anonymity = ""
                iptype = ""
                country = ""
                area = ""
                source = "rmccurdy"
                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_iphai_html(url):
    try:
        html_text = spider_common(url, HEADERS["iphai"], 5, 'utf-8')
        # 0-使用pyquery方式解析
        doc = PyQuery(html_text)
        tr = doc('body > div.container.main-container > div.table-responsive.module > table > tr').items()
        ipInfo_list = []
        for i in tr:
            # ths = i("td").text()
            ths = i("td").text().strip().replace("\n", "")
            if ths != '' or len(ths) != 0:
                print(ths.split(" "))
                ip = ths.split(" ")[0]
                port = ths.split(" ")[1]
                anonymity = ths.split(" ")[2]
                if anonymity == "普匿":
                    anonymity = "1"
                else:
                    anonymity = "2"
                iptype = ths.split(" ")[3]
                if "HTTP" in iptype and "HTTPS" in iptype or iptype == '':
                    iptype = "http"
                country = ths.split(" ")[4]
                if "中国" in country:
                    country = "中国"
                    area = country.replace("中国", "")
                else:
                    country = country
                    area = ""
                source = "iphai"
                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_jiangxianli_html(url):
    try:
        html_text = spider_common(url, HEADERS["jiangxianli"], 5, 'utf-8')
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_jiangxianli_html(url)
            else:
                return
        print(html_text)
        doc = PyQuery(html_text)
        trs = doc(
            "body > div.row > div > div.box > div.box-body.table-responsive.no-padding > table > tbody > tr").items()
        ipInfo_list = []
        for i in trs:
            td_list = i("td").text().split(" ")
            ip = td_list[1]
            port = td_list[2]
            anonymity = td_list[3]
            if anonymity == "透明":
                anonymity = "0"
            elif anonymity == "高匿":
                anonymity = "2"
            else:
                anonymity = "1"
            iptype = td_list[4]
            country = td_list[5]
            if '' in td_list:
                area = ""
            else:
                area = td_list[6] + td_list[7]
            source = "jiangxianli"
            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************

def get_proxylistplus_html(url):
    try:
        html_text = spider_common(url, HEADERS["proxylistplus"], 5, 'utf-8')
        print(html_text)
        doc = PyQuery(html_text)
        h1 = doc('#page > table.bg > tr').items()
        ipInfo_list = []
        for j in h1:
            msg = j('td').text().strip().replace("\n", "")
            if msg != "" or len(msg) != 0:
                ip = msg.split(" ")[0]
                port = msg.split(" ")[1]
                anonymity = msg.split(" ")[2]
                if anonymity == "transparent":
                    anonymity = "0"
                elif anonymity == "elite":
                    anonymity = "1"
                else:
                    anonymity = "2"
                country = msg.split(" ")[3]
                iptype = msg.split(" ")[5]
                if iptype == "yes":
                    iptype = "https"
                else:
                    iptype = "http"
                area = ""
                source = "proxylistplus"
                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_github_html(url):
    try:
        html_text = spider_common(url, HEADERS["githubusercontent"], 5, 'utf-8')
        ipInfo_list = []
        for i in (html_text.split("\n")):
            if i.replace("\n", "").replace(" ", "") != "":
                ip = json.loads(i)["host"]
                country = json.loads(i)["country"]
                try:
                    iptype = json.loads(i)["type"]
                except:
                    iptype = ""
                port = json.loads(i)["port"]
                anonymity = json.loads(i)["anonymity"]
                export_address = tuple(json.loads(i)["export_address"])
                if anonymity == "transparent" or len(export_address) == 2 or "unknown" in export_address:
                    anonymity = 0
                elif anonymity == "anonymous":
                    anonymity = 1
                else:
                    anonymity = 2
                area = ""
                source = "githubusercontent"
                trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
                if trueOrFalse == 1:
                    ipInfo_list.append(
                        {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                         "area": area, "source": source})
                    # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                    # print(prames)
                    # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_thebigproxylist_html(url):
    try:
        html_text = spider_common_ip(PROXIESIP, url, HEADERS["thebigproxylist"], 5, 'utf-8')
        print(html_text)
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text or "404 Not Found" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_thebigproxylist_html(url)
            else:
                return
        ipInfoList = html_text.split("\n")
        ipInfo_list = []
        while '' in ipInfoList:
            ipInfoList.remove('')
        for i in ipInfoList:
            ipInfo = i.split(",")
            ip = ipInfo[0].split(":")[0]
            port = ipInfo[0].split(":")[1]
            anonymity = ""
            iptype = ipInfo[1]
            country = ""
            area = ""
            source = "thebigproxylist"
            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_freeproxylist_html(url):
    try:
        html_text = spider_common(url, HEADERS["free-proxy-list"], 5, 'utf-8')
        doc = PyQuery(html_text)
        tr = doc('body > div.wrapper > div.container > div > div > div.table-responsive > table > tbody > tr').items()
        ipInfo_list = []
        for i in tr:
            ipInfo = i("td").items()
            tdlist = []
            for j in ipInfo:
                tdlist.append(j.text())
            ip = tdlist[0]
            port = tdlist[2]
            country = tdlist[3]
            area = tdlist[4]
            iptype = tdlist[8]
            anonymity = tdlist[9]
            if anonymity == "High Anonymous":
                anonymity = "2"
            source = "free-proxy-list"
            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        # print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************
def get_cnProxy_html(url):
    html_text = spider_common_ip(PROXIESIP, url, HEADERS["cnProxy"], 10, 'utf-8')
    print(html_text)
    try:
        i = 0
        if '''setTimeout("location.replace(location.href.split(\\"#\\")[0])",2000);''' in html_text or "function setCookie(name,value)" in html_text:
            i += 1
            if i != 10:
                time.sleep(5)
                get_cnProxy_html(url)
            else:
                return
        doc = PyQuery(html_text)
        trs = doc("div.table-container > table.sortable > tbody > tr").items()
        ipInfo_list = []
        for i in trs:
            ip_list = i("td").text().split(" ")
            ip = ip_list[0]
            port = ip_list[1]
            anonymity = ""
            iptype = ""
            country = "中国"
            area = ip_list[2]
            source = "cnProxy"
            trueOrFalse = RedisHelperConnect().redis_sadd("proxiesDuplicates", ip)
            if trueOrFalse == 1:
                ipInfo_list.append(
                    {"ip": ip, "port": str(port), "anonymity": str(anonymity), "type": iptype, "country": country,
                     "area": area, "source": source})
                # sql = "insert into proxiesinitial_test(ip,port,anonymity,iptype,country,area,source) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # prames = (ip, str(port), str(anonymity), iptype, country, area, source)
                # print(prames)
                # MysqlHelper("proxiesinitial_test").insert(sql, *prames)
        print(ipInfo_list)
        g = RedisHelperConnect().redis_rpush_batch("proxiesInitial", ipInfo_list)
    except Exception as e:
        print("SPIDER COMMON:", e)


# ***********************************************************************************************************************

def get_ihuan_html(url):
    html_text = spider_common_ip(PROXIESIP, url, HEADERS["ihuan"], 5, 'utf-8')
    print(html_text)
    if "输入验证码证明您不是机器人，输入后可以暂时浏览网站" in html_text:
        time.sleep(5)
        print("需要验证码")
        get_ihuan_html(url)
    else:
        doc = PyQuery(html_text)
        options = doc('div.col-md-10 > div.panel.panel-default > a').items()
        for i in options:
            countryUrl = "https://ip.ihuan.me" + str(i.attr("href"))
            print(countryUrl)


def get_ihuan_ipInfo(url):
    html_text = spider_common_ip(PROXIESIP, url, HEADERS["ihuan"], 5, 'utf-8')
    print(html_text)
    if "输入验证码证明您不是机器人，输入后可以暂时浏览网站" in html_text:
        time.sleep(5)
        print("需要验证码")
        get_ihuan_ipInfo(url)
    else:
        doc = PyQuery(html_text)
        options = doc('div.col-md-10 > div.panel.panel-default > a').items()
        for i in options:
            countryUrl = "https://ip.ihuan.me" + str(i.attr("href"))
            print(countryUrl)


if __name__ == '__main__':
    print("sum:==>", SUM)
