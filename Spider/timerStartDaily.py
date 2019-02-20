#!/usr/bin/env python  
# encoding: utf-8  
""" 
@author: jingjingli 
@software: PyCharm 
@file: timerStartDaily.py.py
@time: 2019/2/14
@describe: proxypool--代理网站爬虫调度及周期更新

"""
import sys
import os
import time
import datetime
import threading
import schedule
from Spider.generateProxiesProcessor import get_qydaili_html
from Spider.generateProxiesProcessor import get_xicidaili_html
from Spider.generateProxiesProcessor import get_data5u_html
from Spider.generateProxiesProcessor import get_66ip_country_html
from Spider.generateProxiesProcessor import get_kuaidaili_html
from Spider.generateProxiesProcessor import get_goubanjia_html
from Spider.generateProxiesProcessor import get_ip3366_html
from Spider.generateProxiesProcessor import get_zdaye_html
from Spider.generateProxiesProcessor import get_89ip_html
from Spider.generateProxiesProcessor import get_xsdaili_html
from Spider.generateProxiesProcessor import get_31f_html
from Spider.generateProxiesProcessor import get_ab57_html
from Spider.generateProxiesProcessor import get_atomintersoft_html
from Spider.generateProxiesProcessor import get_rmccurdy_html
from Spider.generateProxiesProcessor import get_iphai_html
from Spider.generateProxiesProcessor import get_jiangxianli_html
from Spider.generateProxiesProcessor import get_github_html
from Spider.generateProxiesProcessor import get_thebigproxylist_html
from Spider.generateProxiesProcessor import get_freeproxylist_html
from Spider.generateProxiesProcessor import get_cnProxy_html

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


def job_qydaili():
    print("当前正在爬取qydaili")
    url_list = ['unchina', 'china']
    base_url = "http://www.qydaili.com/free/?action="
    for i in url_list:
        temp1_url = base_url + i
        for j in range(1, 5):
            temp2_url = temp1_url + "&page="
            url = temp2_url + str(j)
            get_qydaili_html(url)


def job_xicidaili():
    print("当前正在爬取xicidaili")
    base_url = "https://www.xicidaili.com/"
    url_list = ['nn', 'nt', 'wn', 'wt']
    for i in url_list:
        url = base_url + i
        get_xicidaili_html(url)


def job_data5u():
    base_url = "http://www.data5u.com/free/"
    url_list = ['gngn/index.shtml', 'gnpt/index.shtml', 'gwgn/index.shtml', 'gwpt/index.shtml']
    for i in url_list:
        url = base_url + i
        get_data5u_html(url)


def job_66ip():
    get_66ip_country_html("http://www.66ip.cn/")


def job_kuaidaili():
    start_url = "https://www.kuaidaili.com/ops/proxylist/"
    for i in range(1, 11):
        url = start_url + str(i)
        get_kuaidaili_html(url)


def job_guobanjia():
    get_goubanjia_html("http://www.goubanjia.com/")


def job_ip3366():
    start_url = "http://www.ip3366.net/free/?stype="
    end_url = "&page="
    for i in range(1, 5):
        url = start_url + str(i) + end_url
        for j in range(1, 8):
            time.sleep(2)
            get_ip3366_html(url + str(j))


def job_zdaye():
    get_zdaye_html("http://ip.zdaye.com/dayProxy.html")


def job_89ip():
    for i in range(1, 56):
        start_url = "http://www.89ip.cn/index_"
        end_url = ".html"
        url = start_url + str(i) + end_url
        get_89ip_html(url)


def job_xsdaili():
    get_xsdaili_html("http://www.xsdaili.com/")


def job_31f():
    get_31f_html("http://31f.cn/")


def job_ab57():
    get_ab57_html("http://ab57.ru/downloads/proxyold.txt")


def job_atomintersoft():
    get_atomintersoft_html("http://www.atomintersoft.com/Free_Open_Public_HTTP_Proxies_sorted_by_countries")


def job_rmccurdy():
    get_rmccurdy_html("https://www.rmccurdy.com/scripts/proxy/good.txt")


def job_iphai():
    base_url = "http://www.iphai.com/free/"
    url_list = ['ng', 'np', 'wg', 'wp']
    for i in url_list:
        url = base_url + i
        get_iphai_html(url)


def job_jiangxianli():
    base_url = "http://ip.jiangxianli.com/?page="
    for i in range(1, 5):
        time.sleep(2)
        url = base_url + str(i)
        get_jiangxianli_html(url)


def job_github():
    get_github_html("https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list")


def job_thebigproxylist():
    get_thebigproxylist_html(
        "http://www.thebigproxylist.com/members/proxy-api.php?output=all&user=list&pass=8a544b2637e7a45d1536e34680e11adf")


def job_freeproxylist():
    base_start_url = "https://free-proxy-list.com/?page="
    base_eng_url = "&port=&up_time=0"
    for i in range(1, 6):
        url = base_start_url + str(i) + base_eng_url
        get_freeproxylist_html(url)


def job_cnProxy():
    get_cnProxy_html("https://cn-proxy.com/")


def task_qydaili():
    threading.Thread(target=job_qydaili).start()


def task_xicidaili():
    threading.Thread(target=job_xicidaili).start()


def task_data5u():
    threading.Thread(target=job_data5u).start()


def task_66ip():
    threading.Thread(target=job_66ip).start()


def task_kuaidaili():
    threading.Thread(target=job_kuaidaili).start()


def task_guobanjia():
    threading.Thread(target=job_guobanjia).start()


def task_ip3366():
    threading.Thread(target=job_ip3366).start()


def task_zdaye():
    threading.Thread(target=job_zdaye).start()


def task_89ip():
    threading.Thread(target=job_89ip).start()


def task_xsdaili():
    threading.Thread(target=job_xsdaili).start()


def task_31f():
    threading.Thread(target=job_31f).start()


def task_ab57():
    threading.Thread(target=job_ab57).start()


def task_atomintersoft():
    threading.Thread(target=job_atomintersoft).start()


def task_rmccurdy():
    threading.Thread(target=job_rmccurdy).start()


def task_iphai():
    threading.Thread(target=job_iphai).start()


def task_jiangxianli():
    threading.Thread(target=job_jiangxianli).start()


def task_github():
    threading.Thread(target=job_github).start()


def task_thebigproxylist():
    threading.Thread(target=job_thebigproxylist).start()


def task_freeproxylist():
    threading.Thread(target=job_freeproxylist).start()


def task_cnProxy():
    threading.Thread(target=job_cnProxy).start()


def spider_run():
    # 调度时间都是根据网站更新时间来确定的
    schedule.every(5).minutes.do(task_qydaili)
    schedule.every(10).minutes.do(task_xicidaili)
    schedule.every(2).minutes.do(task_data5u)
    schedule.every(1).hour.do(task_66ip)
    schedule.every(3).minutes.do(task_kuaidaili)
    schedule.every(3).minutes.do(task_guobanjia)
    schedule.every(33).minutes.do(task_ip3366)
    schedule.every(30).minutes.do(task_zdaye)
    schedule.every(1).hour.do(task_89ip)
    schedule.every(5).hours.do(task_xsdaili)
    schedule.every(1).hour.do(task_31f)
    schedule.every(2).hours.do(task_ab57)
    schedule.every(2).hours.do(task_atomintersoft)
    schedule.every(2).hours.do(task_rmccurdy)
    schedule.every(1).hour.do(task_iphai)
    schedule.every(2).minutes.do(task_jiangxianli)
    schedule.every(10).minutes.do(task_github)
    schedule.every(1).hour.do(task_thebigproxylist)
    schedule.every(4).minutes.do(task_freeproxylist)
    schedule.every(1).hour.do(task_cnProxy)

    while True:
        time.sleep(5)
        schedule.run_pending()


if __name__ == '__main__':
    spider_run()
