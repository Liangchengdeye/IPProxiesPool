#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: Api.py 
@time: 2019/1/21 16:56 
@describe: 
"""
import json
import sys
import os
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask, jsonify, request
import threading
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from Scheduler.proxies_Update import proxies_Update_main, proxies_get_number
# 初始化API
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.logger.warning("i am run")


@app.route('/')
def index():
    return '<h1>欢迎查看介绍：</h1>' \
           '<h3>1. 获取一个代理IP：/proxies/get</h3>' \
           '<h3>2. 查看可用代理数量 /proxies/status</h3>' \
           '<h3>3. 获取一个直接可调度IP：/proxies/getip</h3>'


@app.errorhandler(404)
def page_not_found(error):
    return "404"


@app.route('/proxies/404/', methods=['GET'])
def get_404():
    return "i know!"


@app.route('/proxies/live', methods=['GET', 'POST'])
def check_proxies():
    # ?p = 1 & type = 1
    p = request.form.get('p')
    ptype = request.form.get('type')
    print(p, ptype)
    return p


@app.route('/proxies/get', methods=['GET'])
def get_proxies():
    proxies = proxies_Update_main()
    return proxies


@app.route('/proxies/status', methods=['GET'])
def get_status():
    grade10, grade8, grade6, grade4, grade, base = proxies_get_number()
    data = {"GRADE10": grade10, "GRADE8": grade8, "GRADE6": grade6, "GRADE4": grade4, "待检测": grade, "未检测": base}
    return jsonify(data)


@app.route('/proxies/getip', methods=['GET'])
def get_proxies_ip():
    try:
        data = proxies_Update_main()
        proxies = json.loads(data)
        IP = proxies['ip'] + ":" + proxies['port']
        pro = json.dumps({"http": "http://{}".format(IP)}, ensure_ascii=False)
        return pro
    except:
        return "IP POOL IS NULL!"


# 启动API
def run_api():
    # app.run(host='0.0.0.0', port=8020)
    http_server = WSGIServer(('0.0.0.0', 8030), app)
    http_server.serve_forever()


# 线程锁
class Thread_worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global lock
        if lock.acquire():
            lock.release()


def run_start():
    lock = threading.Lock()
    ThreadList = []
    t = Thread_worker()
    ThreadList.append(run_api())
    ThreadList.append()


    t.start()
    t.json()


if __name__ == '__main__':
    run_api()

