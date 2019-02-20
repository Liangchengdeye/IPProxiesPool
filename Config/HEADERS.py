#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: HEADERS.py 
@time: 2018/9/26 17:31 
@describe: 请求头集合--爬虫请求头信息在此配置
'User-Agent': '%s' % UserAgent.pc_agent() 启用轮换浏览器请求头
"""
import os
import sys
sys.path.append(r'your_path')
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from BaseFile.UserAgent import UserAgent

HEADERS = {
    # 百度代理测试
    "baiduTest": {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'no-cache',
        'Host': 'www.baidu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': '%s' % UserAgent.pc_agent()
    },
    # 目标网站测试-Host占位
    "hostUrlTest": {
        'Host': '',
        'User-Agent': '%s' % UserAgent.pc_agent()
    },
    # 旗云代理
    "qydaili": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "__cfduid=d69521af1a98fde17a4ece3aa8da833f51549874980; UM_distinctid=168dbbf38fc44-02dea940aeb1dd-5d1f3b1c-15f900-168dbbf38fd3c3; CNZZDATA1275082454=1291768453-1549874981-null%7C1549874981",
        "Host": "www.qydaili.com",
        "Pragma": "",
        "Referer": "http://www.qydaili.com/free/?action=unchina",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # 西刺代理
    "xicidaili": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWY0YTU3NjdiYTY5YmU0NzI1MDUyYTFlNGM5N2UyYjUyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXlRMGsxcEJPWFJWbUtiN3d4ZTRxekVSc2tsZ2pUQVlCUFNOVlhUYzJPWVU9BjsARg%3D%3D--10aaf67fc52415675e6a1d95b07896a3d81d3e47; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1549880724; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1549880765",
        "Host": "www.xicidaili.com",
        "Pragma": "",
        "Referer": "https://www.xicidaili.com/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # 无忧代理
    "data5u": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "UM_distinctid=1689db4397180c-0d2145846a16ea-5d1f3b1c-15f900-1689db43972472; JSESSIONID=449BAFBA2ED62F747ABACCDF3D12E76F; Hm_lvt_3406180e5d656c4789c6c08b08bf68c2=1548834060,1549895335; CNZZDATA1260383977=1626520922-1548829339-http%253A%252F%252Fwww.data5u.com%252F%7C1549891345; Hm_lpvt_3406180e5d656c4789c6c08b08bf68c2=1549895429",
        "Host": "www.data5u.com",
        "Pragma": "",
        "Referer": "http://www.data5u.com/free/gngn/index.shtml",
        "Upgrade-Insecure-Requests": "1",
        'User-Agent': '%s' % UserAgent.pc_agent()
    },
    # 66代理
    "66ip": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "yd_cookie=9b679713-59d2-43709462f1d2d5c4c1220497b48aec54dd28; _ydclearance=1681067ebae7312383ed4ff8-cb32-4828-96c7-ceed2c490c99-1548740819; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1547105775,1547109921,1548733624; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1548733624",
        "Host": "www.66ip.cn",
        "Pragma": "",
        "Referer": "http://www.66ip.cn/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # k快代理
    "kuaidaili": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "channelid=0; sid=1548817037093374; _ga=GA1.2.2124506962.1548817048; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1548817046,1549938639; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1549938639; _gid=GA1.2.144450665.1549938640; _gat=1",
        "Host": "www.kuaidaili.com",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # goubanjia
    "goubanjia": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        # "Cookie": "UM_distinctid=168362f7b2c332-0d7acd09fcc64f-5d1f3b1c-15f900-168362f7b2d386; JSESSIONID=C3963E4B89ECFAA30DF513BA06F181FA; CNZZDATA1253707717=255616372-1547093242-http%253A%252F%252Fwww.goubanjia.com%252F%7C1547792743",
        "Host": "www.goubanjia.com",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # 云代理
    "ip3366": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "",
        "Connection": "keep-alive",
        # "Cookie": "UM_distinctid=16883f342e782a-07e353b12eaeb3-5d1f3b1c-15f900-16883f342e8324; CNZZDATA1256284042=911408821-1548401977-http%253A%252F%252Fwww.ip3366.net%252F%7C1548409697",
        "Host": "www.ip3366.net",
        "Pragma": "",
        "Referer": "http://www.ip3366.net/free/?stype=1&page=1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # 站大爷
    "zdaye": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "",
        "Connection": "keep-alive",
        # "Cookie": "acw_tc=781bad3615470973291815784e3b3d6f05d6e432f2b5fb3e2b59b4426a4786; ASPSESSIONIDSQSSSTCC=MPCFBJGDGOHFKDILCJANDPKO; __51cke__=; Hm_lvt_8fd158bb3e69c43ab5dd05882cf0b234=1547097376,1547097549; ASPSESSIONIDACCAABRB=EKOPCOHDDKFOBHILCFCBJFFM; ASPSESSIONIDSABQCABT=MADBDICCLEOMOJKANHFNKELG; ASPSESSIONIDQQCDTDDC=LGBIGBGBLKCCNECIOPGEIAHH; acw_sc__v2v3=5c4ac75d98bd620c79671ccb0d3f162b47bf2c2f; acw_sc__v3v2=NWM0YWM3NjAxZTQ5ZTQxNGRmMjYwY2M5ZDdhNGZkMjk0Mzc4YzkwMQ==; __tins__16949115=%7B%22sid%22%3A%201548404498149%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201548406411267%7D; __51laig__=20; Hm_lpvt_8fd158bb3e69c43ab5dd05882cf0b234=1548404613",
        "Host": "ip.zdaye.com",
        "Pragma": "",
        "Referer": "http://ip.zdaye.com/dayProxy.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # 89免费代理
    "89ip": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "",
        "Connection": "keep-alive",
        "Cookie": "yd_cookie=b668203c-1380-42ba854afe01af4421b0118e1f0923b6875f; UM_distinctid=16836355d3813c-01e53956b25fd6-5d1f3b1c-15f900-16836355d3946c; Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829=1547097694; CNZZDATA1254651946=1719768138-1547097693-null%7C1547719486; Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829=1547719614",
        "Host": "www.89ip.cn",
        "Pragma": "",
        "Referer": "http://www.89ip.cn/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # 三一代理
    "31f": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "",
        "Connection": "keep-alive",
        # "Cookie": "Hm_lvt_c04918a39ff11e02096f3cd664c5ada6=1547109123; Hm_lpvt_c04918a39ff11e02096f3cd664c5ada6=1547794799",
        "Host": "31f.cn",
        "Pragma": "",
        "Referer": "http://31f.cn/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()

    },
    # atomintersoft
    "atomintersoft": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "SESS9a657c56e26b186d5dac75fba956499b=tcbl7q3jje4am2f0ga3idjro97; __utmc=2813024; __utmz=2813024.1548228978.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=2813024.1332438806.1548228978.1548228978.1548231780.2; __utmt=1; __utmb=2813024.18.10.1548231780",
        "Host": "www.atomintersoft.com",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # iphai
    "iphai": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "PHPSESSID=58usc6ojdjj3kmdvpasslvl3n7; YII_CSRF_TOKEN=c71d47a14b93306fdea6d2fec476bfb8037d3d25s%3A40%3A%228d3073127c163ae0ee9c920a72e84e79d03869d4%22%3B; Hm_lvt_1528f7f4830b519951a59e6a1656f499=1547457275; safedog-flow-item=83AED3E22285B796E5B346866EA64D40; 5d6fb81d1f871a290099d01c15e4d68d=5fbf9a496afa31f90488da1214db64155b94dd16s%3A8%3A%22%2Ffree%2Fng%22%3B; Hm_lpvt_1528f7f4830b519951a59e6a1656f499=1548123419",
        "Host": "www.iphai.com",
        "Pragma": "",
        "Referer": "http://www.iphai.com/free/wp",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # jiangxianli
    "jiangxianli": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "",
        "Host": "ip.jiangxianli.com",
        "Pragma": "",
        "Referer": "http://ip.jiangxianli.com/?page=1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # github开源
    "githubusercontent": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "",
        "Host": "raw.githubusercontent.com",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()

    },
    # 小河虾
    "xiaohexia": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "",
        "Host": "www.xiaohexia.cn",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # ProxyList
    "proxylistplus": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "",
        # "Cookie": "__cfduid=d5cd8ff733b5e7fc5348c89ebdadc165c1547719589; _ga=GA1.2.1970309085.1547719587; _gid=GA1.2.847130946.1547719587; _jsuid=77619694; _first_pageview=1; no_tracky_100814458=1; __atuvc=2%7C3; __atuvs=5c4183241f278549000",
        "Host": "list.proxylistplus.com",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # The Big Proxy List
    "thebigproxylist": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "",
        "Connection": "keep-alive",
        "Cookie": "__cfduid=d5c32d68a4a9dd8311525cc9f1e73c2361549960920; PHPSESSID=4gae3vdb73e72hho4sg73j8gb0; ref=%5Bhttp%3A//www.thebigproxylist.com/%5D; __utma=148705394.975065658.1549961056.1549961056.1549961056.1; __utmc=148705394; __utmz=148705394.1549961056.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=148705394.4.10.1549961056",
        "Host": "www.thebigproxylist.com",
        "Pragma": "",
        "Referer": "http://www.thebigproxylist.com/members/proxy-api.php?output=all&user=list&pass=8a544b2637e7a45d1536e34680e11adf",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # ProxyList
    "ProxyList": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "",
        "Cookie": "__cfduid=d5cd8ff733b5e7fc5348c89ebdadc165c1547719589; _ga=GA1.2.1970309085.1547719587; _jsuid=77619694; _gid=GA1.2.2147134425.1548040422; no_tracky_100814458=1; _gat=1; _first_pageview=1; __atuvc=3%7C3%2C6%7C4; __atuvs=5c45ab755ca7973c004",
        "Host": "list.proxylistplus.com",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # proxydb
    "proxydb": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.2.1685822590.1547542281; _gid=GA1.2.2090599347.1548209307; _gat=1",
        "Host": "proxydb.net",
        "Pragma": "",
        "Referer": "http://proxydb.net/?country=",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # Free Proxy List
    "free-proxy-list": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "",
        "Cookie": "PHPSESSID=b7463512c0861d18261a58a40fb7190b; _ga=GA1.2.685826152.1548041885; _gid=GA1.2.906372833.1548211307; _gat=1",
        "Host": "free-proxy-list.com",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # rmccurdy
    "rmccurdy": {
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "",
        "Cookie": "__cfduid=dab2c14666447dccfafa1265a5d0a44c41548215275",
        "Host": "www.rmccurdy.com",
        "Pragma": "no-cache",
        "Referer": "https://www.rmccurdy.com/scripts/proxy/good.txt",
        "Upgrade-Insecure-Requests": "",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # ab57
    "ab57": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "",
        "Host": "ab57.ru",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # proxylists
    "proxylists": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "__utmc=204065105; __utmz=204065105.1549955009.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=204065105.196318989.1549955009.1549955009.1550026657.2; __utmt=1; __utmb=204065105.4.10.1550026657",
        "Host": "www.proxylists.net",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # 小舒代理
    "xsdaili": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "",
        "Host": "www.xsdaili.com",
        "Pragma": "",
        "Referer": "http://www.xsdaili.com/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # 小幻HTTP代理
    "ihuan": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "",
        "Cookie": "__cfduid=d5c4d05b953edc04f60c689c04672b85f1547105536; Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829=1547105532; Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829=1548400738",
        "Host": "ip.ihuan.me",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "%s" % UserAgent.pc_agent()
    },
    # 有代理IP
    "youdaili": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "Hm_lvt_f8bdd88d72441a9ad0f8c82db3113a84=1547100133,1548731981; Hm_lpvt_f8bdd88d72441a9ad0f8c82db3113a84=1548732209",
        "Host": "www.youdaili.net",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    },
    # cn-proxy
    "cnProxy": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "",
        "Cookie": "",
        "Host": "cn-proxy.com",
        "Pragma": "",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
}

if __name__ == '__main__':
    print(HEADERS['heasers'])
