import datetime
import random
import re
import json

from bson import ObjectId

from models.web_monitor import model
from turbo.core.exceptions import ResponseMsg
from cPython import cPython as cp
from lib import tools

tb_web_list = model.WebList()
tb_web_log = model.WebLog()


def list(page, limit, search_key, search_value):
    now_time = datetime.datetime.now()
    res = []
    Q = {}
    if search_key and search_value:
        if search_key in ['title', 'desc']:
            Q[search_key] = {'$regex': search_value}
        else:
            Q[search_key] = int(search_value) if tools.isint(search_value) else search_value
    for f in tb_web_list.find(Q).skip((page - 1) * limit).limit(limit).sort('atime', -1):
        f['status24'], f['status24_fail'], f['status24_success'] = get_day_status(f['_id'])
        f['ltime_str'] = tools.sec2hms((now_time - f.get('ltime', now_time)).total_seconds())
        if not f['ltime_str'].endswith('前'):
            f['ltime_str'] += '前'
        res.append(f)
    res.sort(key=lambda k: (k.get('status24', 0)))
    return res, tb_web_list.find(Q).count()


def get_day_status(id):
    datas = tb_web_log.find({'id': id, 'atime': {'$gte': datetime.datetime.now() - datetime.timedelta(days=1)}})
    success, count = 0, 0
    for data in datas:
        count += 1
        success += 0 if data.get('value', 0) == -1 else 1
    if count == 0:
        return 0, 0, 0
    return int(success / count * 100), count - success, success


def add(name, url, rate):
    if tb_web_list.find_one({'name': name}):
        raise ResponseMsg(-1, '已经存在相同名称的监控了')

    if tb_web_list.find_one({'name': url}):
        raise ResponseMsg(-1, '已经存在相同url的监控了')

    tb_web_list.insert({
        'name': name,
        'atime': datetime.datetime.now(),
        'ltime': datetime.datetime(2000, 1, 1),
        'warn_time': None,
        'url': url,
        'con_error_num': 0,
        'enable': True,
        'rate': int(rate),
    })


def edit(id, key, value):
    id = ObjectId(id)
    web_info = tb_web_list.find_by_id(id)
    if tools.isint(value):
        value = int(value)
    if value == 'false':
        value = False
    if value == 'true':
        value = True
    if not web_info:
        raise ResponseMsg(-1, '不存在的监控信息')
    tb_web_list.update({'_id': web_info['_id']}, {'$set': {
        key: value
    }})


def remove(id):
    id = ObjectId(id)
    tb_web_list.remove_by_id(id)


if __name__ == '__main__':
    add('3333', 'https://www.baidu.com', 1)
