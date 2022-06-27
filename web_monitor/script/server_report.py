# -*- coding:utf-8 -*-
# 服务器上报信息
import datetime
import json
import os
import re
from cPython import cPython as cp


def start(test=False):
    _cpu_info = os.popen('cat /proc/cpuinfo | grep siblings').read()
    cpu_siblings = 1
    try:
        cpu_siblings = int(re.findall('(\d{1,3})', _cpu_info)[0])
    except:
        pass
    _ = os.popen('top -bn 1 -i -c').read()
    if test:
        _ = open('t', 'r').read()
    print(_)
    cpu = {
        'use': round(100 - float(cp.get_string(_, 'ni,', 'id').strip()), 2),
        'siblings': cpu_siblings,
    }
    load = [float(f.strip()) for f in cp.get_string(_, 'load average:', '\n').split(',')]

    _ = os.popen('free -b').read()
    if test:
        _ = open('free', 'r').read()
    memory_temp = re.findall('Mem.+?(\d+).+?(\d+).+?(\d+).+?(\d+).+?(\d+).+?(\d+)', _)
    memory_names = [f for f in _.split('\n')[0].split(' ') if f]
    cached_index = 5
    for i, f in enumerate(memory_names):
        if f.find('cache') > -1:
            cached_index = i
            break
    if cached_index == 5:
        memory = int(memory_temp[0][1]) - int(memory_temp[0][cached_index])
    else:
        memory = int(memory_temp[0][1])
    total_memory = int(memory_temp[0][0])
    memory = {
        'value': memory,
        'total_value': total_memory,
    }

    _ = os.popen('df -k').read()
    if test:
        _ = open('disk', 'r').read()

    disk_temp = re.findall('(/dev.+?) ([\d\.]+).+?([\d\.]+).*(/.*)', _)
    disk = []
    for f in disk_temp:
        disk.append({
            'disk_name': f[0].strip(),
            'value': int(f[2]) * 1024,
            'total_value': int(f[1]) * 1024,
            'mount_name': f[3].strip(),
        })
    _ = os.popen('vnstat --json').read()
    if test:
        _ = open('network', 'r').read()
    network = []
    try:
        network_temp = json.loads(_)
        for f in network_temp['interfaces'][0]['traffic']['hours']:
            time = '%s%02d%02d%02d' % (f['date']['year'], f['date']['month'], f['date']['day'], f['id'])
            network.append({
                'time': int(time),
                'value': f['tx'] * 1024,
            })
            pass
    except Exception as e:
        print(e)
        try:
            month = datetime.datetime.now().__format__('%m')
            _ = os.popen('vnstat -d').read()
            if test:
                _ = open('network_d', 'r').read()
            network = []
            _list = re.findall('(' + month + '/\d{1,2}/\d{2,4}).*\d{1,3}.\d{1,2}..iB\D+(\d+.\d{1,2}).([KMGT])iB.+\d{1,3}.\d{1,2}..iB', _)
            if len(_list) == 0:
                _list = re.findall('(\d{2,4}-' + month + '-\d{1,2}).*\d{1,3}.\d{1,2}..iB\D+(\d+.\d{1,2}).([KMGT])iB.+\d{1,3}.\d{1,2}..iB', _)
            for f in _list:
                if f[0].find('-') != -1:
                    time = '%s%02d%02d00' % (int(('20' if len(f[0].split('-')[0]) == 2 else '') + f[0].split('-')[0]), int(f[0].split('-')[1]), int(f[0].split('-')[2]))
                else:
                    time = '%s%02d%02d00' % (int(('20' if len(f[0].split('/')[2]) == 2 else '') + f[0].split('/')[2]), int(f[0].split('/')[0]), int(f[0].split('/')[1]))
                value = float(f[1])
                type = f[2]
                if type == 'K':
                    value *= 1024
                if type == 'M':
                    value = value * 1024 * 1024
                if type == 'G':
                    value = value * 1024 * 1024 * 1024
                if type == 'T':
                    value = value * 1024 * 1024 * 1024 * 1024
                network.append({
                    'time': int(time),
                    'value': value,
                })
        except Exception as ee:
            print('not vnstat', ee)

    all = {
        'cpu': cpu,
        'load': load,
        'memory': memory,
        'disk': disk,
        'network': network,
    }
    if test:
        print(all)
        print(cp.post_for_request('https://8861.mac.xiaoc.cn/server_report/all', _data={'data': json.dumps(all)}))
    else:
        print(all)
        print(cp.post_for_request('http://web-monitor.xiaoc.cn:1023/server_report/all', _data={'data': json.dumps(all)}))


if __name__ == '__main__':
    start(False)
