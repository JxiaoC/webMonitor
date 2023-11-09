# -*- coding:utf-8 -*-
import datetime
import json
import threading
import time

import requests
try:
    import realpath
except:
    pass
import os
from helpers.web_monitor import setting
from models.web_monitor import model
from lib import tools
from web_monitor.task import callback

count = os.popen('ps aux | grep http_monitor | grep -v grep | grep -v /bin/sh | wc -l').read()
if int(count) > 1:
    print('is running')
    exit(0)

tb_web_list = model.WebList()
tb_web_log = model.WebLog()

count = tb_web_list.count_documents({'enable': True})
complete_count = 0
lock = threading.RLock()
max_error = 2
run_time_sec = 0


def get_http_code_and_content(url, method='GET', headers=None, data=None):
    try:
        response = requests.request(method.upper(), url, headers=headers, timeout=30, data=data)
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


def monitor(id, info, test=False):
    global complete_count
    try:
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
        callback_url = info.get('callback_url', '')
        con_error_num = info.get('con_error_num', 0)
        warn_time = info.get('warn_time', datetime.datetime(2000, 1, 1))
        push_warn_time = info.get('push_warn_time', datetime.datetime(2000, 1, 1))
        if warn_time is None:
            warn_time = datetime.datetime(2000, 1, 1)
        if push_warn_time is None:
            push_warn_time = datetime.datetime(2000, 1, 1)

        s_time = int(time.time() * 1000)
        http_code, http_content, err_data = get_http_code_and_content(url, method=method, headers=header, data=data)

        if datetime.datetime.now().hour == 3:
            print('3点, 不工作~')
            lock.acquire()
            complete_count += 1
            lock.release()
            return
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
        if test:
            lock.acquire()
            print(url, 'run_time', run_time, 'http_code', http_code)
            complete_count += 1
            lock.release()
            return fail, http_code, run_time, err_data, http_content
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

        continue_sec = (datetime.datetime.now() - warn_time).total_seconds()
        last_sec = (datetime.datetime.now() - push_warn_time).total_seconds()
        max_error_num = setting.get().get('max_error_num', 3)
        if con_error_num >= max_error_num:
            print('报警')
            if last_sec > setting.get().get('silence_time', 60) * 60:
                if con_error_num == max_error_num:
                    # 第一次报警, 记录报警开始时间
                    U['warn_time'] = datetime.datetime.now()
                U['push_warn_time'] = datetime.datetime.now()

                continue_sec = (datetime.datetime.now() - U.get('warn_time', warn_time)).total_seconds()
                tools.send_server_jiang_msg('%s 可用性报警' % name, '站点 %s 发生可用性报警, 已经连续%s次请求失败, 已持续%s' % (url, con_error_num, tools.sec2hms(continue_sec)))
            else:
                print('沉默, 距离上一次警告过去了%ss' % last_sec)
            callback.new_callback(id, callback_url, False)

        if not fail and info.get('con_error_num', 0) >= max_error_num:
            print('警报解除')
            U['warn_time'] = datetime.datetime(2000, 1, 1)
            U['push_warn_time'] = datetime.datetime(2000, 1, 1)
            if tb_web_list.count_documents({'enable': True, 'con_error_num': {'$gt': 0}}) == 1:
                tools.send_server_jiang_msg('%s 全部可用性恢复' % name, '站点 %s 可用性故障已于%s后恢复, 共连续失败%s次' % (
                url, tools.sec2hms(continue_sec), info.get('con_error_num', 0)))
            else:
                tools.send_server_jiang_msg('%s 可用性恢复' % name, '站点 %s 可用性故障已于%s后恢复, 共连续失败%s次' % (
                url, tools.sec2hms(continue_sec), info.get('con_error_num', 0)))
            callback.new_callback(id, callback_url, True)
        tb_web_list.update({'_id': id}, {'$set': U})
        print(url, 'run_time', run_time, 'http_code', http_code)
    except Exception as e:
        print(e)
    lock.acquire()
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
    time.sleep(0.2)

while complete_count < count and run_time_sec < 180:
    run_time_sec += 1
    time.sleep(1)

if run_time_sec >= 180:
    print('run_time_sec out')
print(complete_count)
