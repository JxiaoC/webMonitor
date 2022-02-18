import datetime
import os
import random
import re
import json
import threading
import time

from bson import ObjectId

from models.web_monitor import model
from turbo.core.exceptions import ResponseMsg
from cPython import cPython as cp
from lib import tools

tb_host_list = model.HostExpireList()


def list(page, limit, search_key, search_value):
    now_time = datetime.datetime.now()
    res = []
    Q = {}
    if search_key and search_value:
        if search_key in ['title', 'desc']:
            Q[search_key] = {'$regex': search_value}
        else:
            Q[search_key] = int(search_value) if tools.isint(search_value) else search_value
    for f in tb_host_list.find(Q).skip((page - 1) * limit).limit(limit).sort([('enable', -1), ('rst_time', 1)]):
        f['rst_day'] = int((f.get('rst_time', now_time) - now_time).total_seconds() / 86400)
        f['ltime_str'] = tools.sec2hms((now_time - f.get('ltime', now_time)).total_seconds())
        if not f['ltime_str'].endswith('前'):
            f['ltime_str'] += '前'
        res.append(f)
    return res, tb_host_list.find(Q).count()


def add(name, host):
    if tb_host_list.find_one({'name': name}):
        raise ResponseMsg(-1, '已经存在相同名称的监控了')

    if tb_host_list.find_one({'host': host}):
        raise ResponseMsg(-1, '已经存在相同域名的监控了')
    doc = {
        '_id': ObjectId(),
        'name': name,
        'atime': datetime.datetime.now(),
        'ltime': datetime.datetime(2000, 1, 1),
        'host': host,
        'rst_time': datetime.datetime.now(),
        'enable': True,
    }
    tb_host_list.insert(doc)
    time.sleep(0.5)
    threading.Thread(target=ref_expire_time, args=(doc,)).start()


def edit(id, key, value):
    id = ObjectId(id)
    host_info = tb_host_list.find_by_id(id)
    if tools.isint(value):
        value = int(value)
    if value == 'false':
        value = False
    if value == 'true':
        value = True
    if not host_info:
        raise ResponseMsg(-1, '不存在的监控信息')
    tb_host_list.update({'_id': host_info['_id']}, {'$set': {
        key: value
    }})


def ref_expire_time(data):
    if ObjectId.is_valid(data):
        host_info = tb_host_list.find_by_id(data)
    elif isinstance(data, dict):
        host_info = data
    else:
        raise ResponseMsg(-1, '不存在的监控信息')

    id = host_info.get('_id')
    if not host_info:
        raise ResponseMsg(-1, '不存在的监控信息')
    host = host_info.get('host', '')
    rst = tools.get_host_expire(host)
    tb_host_list.update({'_id': ObjectId(id)}, {'$set': {
        'rst_time': rst,
        'ltime': datetime.datetime.now(),
    }})
    return rst


def ref_all():
    for f in tb_host_list.find({'enable': True}):
        try:
            ref_expire_time(f['_id'])
        except Exception as e:
            print(e)
        print(f)


def remove(id):
    id = ObjectId(id)
    tb_host_list.remove_by_id(id)


if __name__ == '__main__':
    # add('33333', 'www.qq.com')
    # print(list(1, 666, '', ''))
    # ref_expire_time('61bb1210ace2456c1b5dc132')
    ref_all()