# -*- coding:utf-8 -*-
# 服务器上报信息
import json
import os
import re
from cPython import cPython as cp


def start(test=False):
    _ = os.popen('top -bn 1 -i -c').read()
    if test:
        _ = open('t', 'r').read()
    cpu = round(100 - float(cp.get_string(_, 'ni,', 'id').strip()), 2)
    load = [float(f.strip()) for f in cp.get_string(_, 'load average:', '\n').split(',')]
    memory_temp = re.search('(.)iB Mem.+?(\d+?\.\d+?).+?total.+?(\d+?\.\d+?).+?free', _)
    memory = float(memory_temp.group(3))
    total_memory = float(memory_temp.group(2))
    if memory_temp.group(1) == 'K':
        memory *= 1024
        total_memory *= 1024
    if memory_temp.group(1) == 'M':
        memory *= 1024
        memory *= 1024
        total_memory *= 1024
        total_memory *= 1024
    if memory_temp.group(1) == 'G':
        memory *= 1024
        memory *= 1024
        memory *= 1024
        total_memory *= 1024
        total_memory *= 1024
        total_memory *= 1024
    memory = int(memory)
    total_memory = int(total_memory)
    memory = {
        'value': memory,
        'total_value': total_memory,
    }

    _ = os.popen('df -h').read()
    if test:
        _ = open('disk', 'r').read()

    disk_temp = re.findall('(/dev.+?) ([\d\.]+?)G.+?([\d\.]+?)G.*(/.*)', _)
    disk = []
    for f in disk_temp:
        disk.append({
            'disk_name': f[0].strip(),
            'value': int(f[2]) * 1024 * 1024 * 1024,
            'total_value': int(f[1]) * 1024 * 1024 * 1024,
            'mount_name': f[3].strip(),
        })
    # 04/01/2022    23.23 GiB |   25.09 GiB |   48.32 GiB |    4.80 Mbit/s
    _ = os.popen('vnstat --json').read()
    if test:
        _ = open('network', 'r').read()
    network_temp = json.loads(_)
    network = []
    for f in network_temp['interfaces'][0]['traffic']['hours']:
        time = '%s%02d%02d%02d' % (f['date']['year'], f['date']['month'], f['date']['day'], f['id'])
        network.append({
            'time': int(time),
            'value': f['tx'],
        })
        pass

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


if __name__ == '__main__':
    start(True)
