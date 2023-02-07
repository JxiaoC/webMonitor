import base64
import datetime
import json
import time

from bson import ObjectId
from turbo.core.exceptions import ResponseMsg
from models.web_monitor import model

from lib import tools

server_ip = []
server_info = {}
tb_alias = model.ServerMonitorAlias()


def get():
    alias = {}
    for f in tb_alias.find():
        alias[f['ip']] = f['name']
    res = []
    for ip in server_ip:
        _ = json.loads(server_info[ip])
        _['name'] = alias.get(ip, ip)
        _['ip'] = ip
        res.append(_)
    return res


def add(ip, data):
    json_data = json.loads(data)
    if json_data.get('ip', '') != 'auto':
        ip = json_data.get('ip', '')
    if ip not in server_ip:
        server_ip.append(ip)
    server_info[ip] = data


def alias(ip, name):
    if tb_alias.find_one({'ip': ip}):
        tb_alias.update({'ip': ip}, {'$set': {
            'name': name
        }})
    else:
        tb_alias.insert({
            'ip': ip,
            'name': name
        })
