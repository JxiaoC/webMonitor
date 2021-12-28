# -*- coding:utf-8 -*-
import datetime
import json
import threading
import time

import requests

import realpath
from helpers.web_monitor import setting
from models.web_monitor import model
from lib import tools

tb_web_list = model.WebList()
tb_web_log = model.WebLog()

count = tb_web_list.count_documents({'enable': True})
complete_count = 0
lock = threading.RLock()


def get_http_code_and_content(url, method='GET', headers=None, data=None):
    try:
        response = requests.request(method.upper(), url, headers=headers, timeout=60, data=data)
        try:
            content = response.content.decode()
        except:
            content = str(response.content)
        return response.status_code, content, ''
    except Exception as e:
        if str(e).find('Read timed out') > -1:
            return 600, '', str(e)
        else:
            return 601, '', str(e)


def monitor(id, info):
    global complete_count
    now_time = datetime.datetime.now()
    name = info.get('name', '')
    url = info.get('url', '')
    allow_http_code = info.get('allow_http_code', [200])
    header = json.loads(info.get('header', '{}'))
    data = info.get('data', '')
    find_str = info.get('find_str', '')
    find_str_type = info.get('find_str_type', 0)
    method = info.get('method', 'GET')
    if not method:
        method = 'GET'
    con_error_num = info.get('con_error_num', 0)
    warn_time = info.get('warn_time', datetime.datetime(2000, 1, 1))
    if warn_time is None:
        warn_time = datetime.datetime(2000, 1, 1)

    s_time = int(time.time() * 1000)
    http_code, http_content, err_data = get_http_code_and_content(url, method=method, headers=header, data=data)
    fail = http_code not in allow_http_code
    if not fail and find_str:
        if find_str_type == 0 and http_content.find(find_str) == -1:
            fail = True
            http_code = 602
        elif find_str_type == 1 and http_content.find(find_str) > -1:
            fail = True
            http_code = 603

    if fail:
        con_error_num += 1
    else:
        con_error_num = 0
    run_time = int(time.time() * 1000 - s_time)
    tb_web_log.insert({
        'id': id,
        'atime': now_time,
        'http_code': http_code,
        'value': run_time,
        'err_data': err_data,
    })

    U = {
        'ltime': datetime.datetime.now(),
        'con_error_num': con_error_num,
    }

    last_sec = (datetime.datetime.now() - warn_time).total_seconds()
    max_error_num = setting.get().get('max_error_num', 3)
    if con_error_num >= max_error_num:
        print('报警')
        if last_sec > setting.get().get('silence_time', 60) * 60:
            U['warn_time'] = datetime.datetime.now()
            tools.send_server_jiang_msg('%s 可用性报警' % name, '站点 %s 发生可用性报警, 已经连续%s次请求失败' % (url, con_error_num))
        else:
            print('沉默, 距离上一次警告过去了%ss' % last_sec)

    if not fail and info.get('con_error_num', 0) >= max_error_num:
        print('警报解除')
        U['warn_time'] = datetime.datetime(2020, 1, 1)
        tools.send_server_jiang_msg('%s 可用性恢复' % name, '站点 %s 可用性故障已于%s后恢复, 共连续失败%s次' % (url, tools.sec2hms(last_sec), info.get('con_error_num', 0)))
    tb_web_list.update({'_id': id}, {'$set': U})

    lock.acquire()
    print(url, 'run_time', run_time, 'http_code', http_code)
    complete_count += 1
    lock.release()


if get_http_code_and_content('https://www.baidu.com')[0] != 200:
    print('本地无网络访问, 跳过监控')
    exit(0)

for f in tb_web_list.find({'enable': True}):
    now_time = datetime.datetime.now()
    info = tb_web_list.find_by_id(f['_id'])
    ltime = info.get('ltime', now_time)
    rate = info.get('rate', 1)
    if (now_time - ltime).total_seconds() < rate * 60:
        print(f['_id'], '距离上一次监控时间不足%s分钟' % rate)
        complete_count += 1
        continue
    threading.Thread(target=monitor, args=(f['_id'], info)).start()
    time.sleep(1)

while complete_count < count:
    time.sleep(1)

print(complete_count)
