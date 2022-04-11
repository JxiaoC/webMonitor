import base64
import datetime
import json
import time

from bson import ObjectId
from turbo.core.exceptions import ResponseMsg

from lib import tools
from models.web_monitor import model

tb_server_list = model.ServerList()
tb_load_log = model.ServerLoadLog()
tb_cpu_log = model.ServerCPULog()
tb_disk_log = model.ServerDiskLog()
tb_memory_log = model.ServerMemoryLog()
tb_network_log = model.ServerNetworkLog()


def lists(page, limit, search_key, search_value):
    res = []
    Q = {}
    if search_key and search_value:
        if search_key in ['title', 'desc']:
            Q[search_key] = {'$regex': search_value}
        else:
            Q[search_key] = int(search_value) if tools.isint(search_value) else search_value
    for f in tb_server_list.find(Q).skip((page - 1) * limit).limit(limit).sort('atime', -1):
        f['cpu'] = list(tb_cpu_log.find({'id': f['_id']}).sort('atime', -1).limit(1))
        f['cpu'] = f['cpu'][0].get('value', 0) if len(f['cpu']) > 0 else 0

        f['load'] = list(tb_load_log.find({'id': f['_id']}).sort('atime', -1).limit(1))
        f['load'] = {
            'load_1': float(f['load'][0].get('value', '').split(',')[0]) if len(f['load']) > 0 else 0,
            'load_5': float(f['load'][0].get('value', '').split(',')[1]) if len(f['load']) > 0 else 0,
            'load_15': float(f['load'][0].get('value', '').split(',')[2]) if len(f['load']) > 0 else 0,
        }

        f['memory'] = list(tb_cpu_log.find({'id': f['_id']}).sort('atime', -1).limit(1))
        f['memory'] = {
            'value': f['memory'][0].get('value', 0) if len(f['memory']) > 0 else 0,
            'total_value': f['memory'][0].get('total_value', 0) if len(f['memory']) > 0 else 0,
        }

        f['network'] = list(tb_network_log.find({'id': f['_id']}).sort('atime', -1).limit(1))
        f['network'] = f['network'][0].get('value', 0) if len(f['network']) > 0 else 0

        f['disk'] = list(tb_disk_log.find({'id': f['_id']}).sort('atime', -1).limit(30))
        _ = []
        pass_keys = []
        for ff in f['disk']:
            if ff.get('name', 0) in pass_keys:
                continue
            _.append({
                'name': ff.get('name', 0),
                'value': ff.get('value', 0),
                'total_value': ff.get('total_value', 0),
            })
            pass_keys.append(ff.get('name', 0))
        f['disk'] = _
        res.append(f)

    return res, tb_server_list.find(Q).count()


def add(name, ip, desc):
    if tb_server_list.find_one({'name': name}):
        raise ResponseMsg(-1, '已经存在相同名称的监控了')

    tb_server_list.insert({
        'name': name,
        'ip': ip,
        'desc': desc,
        'atime': datetime.datetime.now(),
        'utime': datetime.datetime.now(),
    })


def edit(id, name, ip, desc):
    id = ObjectId(id)
    server_info = tb_server_list.find_by_id(id)
    if not server_info:
        raise ResponseMsg(-1, '不存在的监控信息')
    tb_server_list.update({'_id': server_info['_id']}, {'$set': {
        'name': name,
        'ip': ip,
        'desc': desc,
        'utime': datetime.datetime.now(),
    }})


def remove(id):
    id = ObjectId(id)
    tb_server_list.remove_by_id(id)


def add_cpu_log(id, value):
    id = ObjectId(id)
    value = float(value)
    tb_cpu_log.insert({
        'id': id,
        'value': value,
        'atime': datetime.datetime.now(),
    })


def add_load_log(id, value):
    id = ObjectId(id)
    tb_load_log.insert({
        'id': id,
        'value': value,
        'atime': datetime.datetime.now(),
    })


def add_memory_log(id, value, total_value):
    id = ObjectId(id)
    value = int(value)
    total_value = int(total_value)
    tb_memory_log.insert({
        'id': id,
        'value': value,
        'total_value': total_value,
        'atime': datetime.datetime.now(),
    })


def add_disk_log(id, disk_name, mount_name, value, total_value):
    id = ObjectId(id)
    value = int(value)
    total_value = int(total_value)
    tb_disk_log.insert({
        'id': id,
        'disk_name': disk_name,
        'mount_name': mount_name,
        'value': value,
        'total_value': total_value,
        'atime': datetime.datetime.now(),
    })


def add_network_log(id, time, type, value):
    id = ObjectId(id)
    time = int(time)
    value = int(value)
    tb_network_log.insert({
        'id': id,
        'time': time,
        'value': value,
        'type': type,
        'atime': datetime.datetime.now(),
    })


def add_all(ip, data):
    server_info = tb_server_list.find_one({'ip': ip})
    if not server_info:
        raise ResponseMsg(-1, '不存在的服务器信息, ip匹配的ip%s' % ip)
    id = server_info['_id']
    data = json.loads(data)

    tb_server_list.update({'_id': id}, {'$set': {
        'utime': datetime.datetime.now(),
    }})


if __name__ == '__main__':
    pass
