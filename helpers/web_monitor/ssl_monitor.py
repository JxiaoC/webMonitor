import datetime
import os
import random
import re
import json

from bson import ObjectId

from models.web_monitor import model
from turbo.core.exceptions import ResponseMsg
from cPython import cPython as cp
from lib import tools

tb_ssl_list = model.SSLList()


def list(page, limit, search_key, search_value):
    res = []
    Q = {}
    if search_key and search_value:
        if search_key in ['title', 'desc']:
            Q[search_key] = {'$regex': search_value}
        else:
            Q[search_key] = int(search_value) if tools.isint(search_value) else search_value
    for f in tb_ssl_list.find(Q).skip((page - 1) * limit).limit(limit).sort('atime', -1):
        f['rst_day'] = int((f.get('rst_time', datetime.datetime.now()) - datetime.datetime.now()).total_seconds() / 86400)
        res.append(f)
    return res, tb_ssl_list.find(Q).count()


def add(name, host):
    if tb_ssl_list.find_one({'name': name}):
        raise ResponseMsg(-1, '已经存在相同名称的监控了')

    if tb_ssl_list.find_one({'host': host}):
        raise ResponseMsg(-1, '已经存在相同域名的监控了')

    tb_ssl_list.insert({
        'name': name,
        'atime': datetime.datetime.now(),
        'ltime': datetime.datetime(2000, 1, 1),
        'host': host,
        'rst_time': datetime.datetime.now(),
        'enable': True,
    })


def edit(id, key, value):
    id = ObjectId(id)
    ssl_info = tb_ssl_list.find_by_id(id)
    if tools.isint(value):
        value = int(value)
    if value == 'false':
        value = False
    if value == 'true':
        value = True
    if not ssl_info:
        raise ResponseMsg(-1, '不存在的监控信息')
    tb_ssl_list.update({'_id': ssl_info['_id']}, {'$set': {
        key: value
    }})


def ref_ssl_time(id):
    ssl_info = tb_ssl_list.find_by_id(id)
    if not ssl_info:
        raise ResponseMsg(-1, '不存在的监控信息')
    host = ssl_info.get('host', '')
    data = os.popen("echo | openssl s_client -servername %s  -connect %s:443 2>/dev/null | openssl x509 -noout -dates |grep 'After'| awk -F '=' '{print $2}'| awk -F ' +' '{print $1,$2,$4 }'" % (host, host)).read().strip()
    rst = datetime.datetime.strptime(data, '%b %d %Y')
    tb_ssl_list.update({'_id': ObjectId(id)}, {'$set': {
        'rst_time': rst
    }})
    return rst


def ref_all():
    for f in tb_ssl_list.find({'enable': True}):
        try:
            ref_ssl_time(f['_id'])
        except Exception as e:
            print(e)
        print(f)


def remove(id):
    id = ObjectId(id)
    tb_ssl_list.remove_by_id(id)


if __name__ == '__main__':
    # add('33333', 'www.qq.com')
    # print(list(1, 666, '', ''))
    # ref_ssl_time('61bb1210ace2456c1b5dc132')
    ref_all()