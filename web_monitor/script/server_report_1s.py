# -*- coding:utf-8 -*-
# 服务器实时上报
import datetime
import json
import os
import re
import subprocess
import threading
import time

from cPython import cPython as cp

network_rx = 0  # 接收
network_tx = 0  # 发送
io_read = 0
io_write = 0

def get_cpu_info():
    _cpu_info = os.popen('cat /proc/cpuinfo | grep siblings').read()
    cpu_siblings = 1
    try:
        cpu_siblings = int(re.findall('(\d{1,3})', _cpu_info)[0])
    except:
        pass
    _ = os.popen('top -bn 1 -i -c').read()
    cpu = {
        'use': round(100 - float(cp.get_string(_, 'ni,', 'id').strip()), 2),
        'siblings': cpu_siblings,
    }
    load = [float(f.strip()) for f in cp.get_string(_, 'load average:', '\n').split(',')]
    return cpu, load


def get_memory_info():
    _ = os.popen('free -b').read()
    memory_temp = re.findall('Mem.+?(\d+).+?(\d+).+?(\d+).+?(\d+).+?(\d+).+?(\d+)', _)[0]
    memory_datas = {}
    memory_names_t = [f for f in _.split('\n')[0].split(' ') if f]
    for i, f in enumerate(memory_names_t):
        memory_datas[f] = int(memory_temp[i])
    total = memory_datas.get('total', 0)
    available = 0
    if 'available' in memory_datas.keys():
        available = memory_datas.get('available', 0)
    else:
        available = total - (memory_datas.get('used', 0) - memory_datas.get('buffers', 0) - memory_datas.get('cached', 0))
    return total, available


def thread_get_network_sec():
    global network_tx, network_rx
    while True:
        try:
            datas = {}
            names = []
            process = subprocess.Popen('sar -n DEV 1', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            while process.poll() is None:
                line = process.stdout.readline()
                line = line.strip()
                if line:
                    line = line.decode('gb2312', 'ignore')
                    if line.lower().find('iface') > -1:
                        network_rx = 0
                        network_tx = 0
                        names = [f for i, f in enumerate(line.split(' ')) if f and i > 0]
                        for name in names:
                            if name:
                                datas[name] = 0

                    if line.find('lo') > -1:
                        continue
                    _ = [ff for i, ff in enumerate(line.split(' ')) if ff and i > 0]
                    for i, ff in enumerate(names):
                        try:
                            datas[ff] += float(_[i])
                        except:
                            pass
                    network_rx = int(datas.get('rxkB/s', 0) * 1024)
                    network_tx = int(datas.get('txkB/s', 0) * 1024)
        except Exception as e:
            print(e)
            time.sleep(10)


def get_network_info():
    return network_rx, network_tx


def thread_get_io_sec():
    global io_write, io_read
    while True:
        try:
            datas = {}
            names = []
            process = subprocess.Popen('sar -b 1', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            while process.poll() is None:
                line = process.stdout.readline()
                line = line.strip()
                if line:
                    line = line.decode('gb2312', 'ignore')
                    if line.lower().find('tps') > -1:
                        names = [f for i, f in enumerate(line.split(' ')) if f and i > 0]
                        for name in names:
                            if name:
                                datas[name] = 0

                    _ = [ff for i, ff in enumerate(line.split(' ')) if ff and i > 0]
                    for i, ff in enumerate(names):
                        try:
                            datas[ff] = float(_[i])
                        except:
                            pass
                    io_write = int(datas.get('bwrtn/s', 0))
                    io_read = int(datas.get('bread/s', 0))
        except Exception as e:
            print(e)
            time.sleep(10)


def get_io_info():
    return io_write, io_read


def start():
    while True:
        try:
            cpu, load = get_cpu_info()
            memory_total, memory_available = get_memory_info()
            network_rx, network_tx = get_network_info()
            io_write, io_read = get_io_info()
            data = {
                'cpu': cpu,
                'load': load,
                'memory': {
                    'total': memory_total,
                    'available': memory_available,
                },
                'network': {
                    'rx': network_rx,
                    'tx': network_tx,
                },
                'io': {
                    'write': io_write,
                    'read': io_read,
                },
            }
            print(data)
            print(cp.post_for_request('http://8861.mac.xiaoc.cn/server_report_real/all', _data={'data': json.dumps(data)}))
        except Exception as e:
            print(e)
        time.sleep(1)
    pass


if __name__ == '__main__':
    t = os.popen('sar -b 1 1').read()
    if t.lower().find('average') > -1:
        threading.Thread(target=thread_get_network_sec).start()
        threading.Thread(target=thread_get_io_sec).start()
        time.sleep(2)
    else:
        print('没有安装sysstat, 无法监测网络和磁盘IO信息')
        print(t)
        network_rx = network_tx = io_write = io_read = -1
    start()
