import base64
import datetime
import json
import time

from bson import ObjectId
from turbo.core.exceptions import ResponseMsg

from lib import tools
from models.web_monitor import model
from cPython import cPython as cp

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
        f['status24_list'], f['status24'] = get_day_status(f['_id'])
        f['ltime_str'] = tools.sec2hms((now_time - f.get('ltime', now_time)).total_seconds())
        if not f['ltime_str'].endswith('前'):
            f['ltime_str'] += '前'
        f['_id'] = str(f['_id'])
        f['atime'] = cp.datetime_2_unixtime(f.get('atime', datetime.datetime.now())) if f.get('atime', None) else 0
        f['ltime'] = cp.datetime_2_unixtime(f.get('ltime', datetime.datetime.now())) if f.get('ltime', None) else 0
        f['warn_time'] = cp.datetime_2_unixtime(f.get('warn_time', datetime.datetime.now())) if f.get('warn_time', None) else 0
        f['push_warn_time'] = cp.datetime_2_unixtime(f.get('push_warn_time', datetime.datetime.now())) if f.get('push_warn_time', None) else 0
        res.append(f)
    res.sort(key=lambda k: (k.get('status24', 0)))
    return res, tb_web_list.find(Q).count()


def get_day_status(id):
    id = ObjectId(id)
    web_info = tb_web_list.find_by_id(id)
    datas = tb_web_log.find({'id': id, 'atime': {'$gte': datetime.datetime.now() - datetime.timedelta(days=1)}}).sort('atime', -1).limit(100)
    res = []
    success, count = 0, 0
    for data in datas:
        count += 1
        success += 0 if data.get('http_code', 200) not in web_info.get('allow_http_code', [200]) else 1
        res.append({
            'http_code': data.get('http_code', 200),
            'normal': False if data.get('http_code', 200) not in web_info.get('allow_http_code', [200]) else True,
            'delay': data.get('value', 0),
            'err_data': data.get('err_data', ''),
            'atime': cp.datetime_2_unixtime(data.get('atime', 0)),
            'id': str(data.get('_id', '')),
        })
    if count == 0:
        return res, 0
    return res, int(success / count * 100)
    #     if count == 0:
    #         return res, 0, 0
    # return int(success / count * 100), count - success, success


def add(name, url, rate, method, header, data, allow_http_code, find_str, find_str_type):
    if tb_web_list.find_one({'name': name}):
        raise ResponseMsg(-1, '已经存在相同名称的监控了')

    if tb_web_list.find_one({'name': url}):
        raise ResponseMsg(-1, '已经存在相同url的监控了')

    if method.upper() not in ['GET', 'POST']:
        raise ResponseMsg(-1, 'method只支持get或post')

    headers = {}
    if data == 'dW5kZWZpbmVk':
        data = ''
    if data:
        data = base64.decodebytes(data.encode()).decode()

    if header:
        header = base64.decodebytes(header.encode()).decode()

        try:
            for f in header.split('\n'):
                if f.strip():
                    headers[f.split(':')[0]] = f.replace(f.split(':')[0]+':', '').strip()
        except:
            raise ResponseMsg(-1, '错误的header')

    tb_web_list.insert({
        'name': name,
        'atime': datetime.datetime.now(),
        'ltime': datetime.datetime(2000, 1, 1),
        'warn_time': None,
        'url': url,
        'method': method,
        'con_error_num': 0,
        'enable': True,
        'header': json.dumps(headers),
        'find_str': find_str,
        'find_str_type': int(find_str_type),
        'data': data,
        'allow_http_code': [int(f) for f in allow_http_code.split(',') if f],
        'rate': int(rate),
    })


def edit_all(id, rate, method, header, data, allow_http_code, find_str, find_str_type):
    id = ObjectId(id)
    web_info = tb_web_list.find_by_id(id)
    if not web_info:
        raise ResponseMsg(-1, '不存在的监控信息')

    if data == 'dW5kZWZpbmVk':
        data = ''
    if data:
        data = base64.decodebytes(data.encode()).decode()

    headers = {}
    if header:
        header = base64.decodebytes(header.encode()).decode()

        try:
            for f in header.split('\n'):
                if f.strip():
                    headers[f.split(':')[0]] = f.replace(f.split(':')[0] + ':', '').strip()
        except:
            raise ResponseMsg(-1, '错误的header')

    tb_web_list.update({'_id': id}, {'$set': {
        'header': json.dumps(headers),
        'find_str': find_str,
        'find_str_type': int(find_str_type),
        'data': data,
        'method': method,
        'allow_http_code': [int(f) for f in allow_http_code.split(',') if f],
        'rate': int(rate),
    }})


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
    pass
