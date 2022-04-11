# -*- coding:utf-8 -*-
# 筛选有问题的ip
import os
import re

path = '/var/log/nginx/service.avatar.adesk.com.log'
file = open(path, 'r')
ips = []
ips_count = {}

while True:
        text_line = file.readline()
        if text_line:
            if text_line.lower().find('chrome') > -1:
                ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text_line)[0]
                if ip not in ips:
                    ips_count[ip] = 1
                    ips.append(ip)
                else:
                    ips_count[ip] += 1
                    # print(len(ips), ip)
        else:
            break
ips_count = sorted(ips_count.items(), key=lambda kv:(kv[1], kv[0]))
for f in ips_count:
    if f[1] > 20:
        print(f[0], f[1])