# -*- coding:utf-8 -*-
import datetime

import realpath
from helpers.web_monitor import setting, ssl_monitor
from models.web_monitor import model
from lib import tools

tb_ssl_list = model.SSLList()
ssl_min_day = int(setting.get().get('ssl_min_day', '1'))
total = 0
send_msg = ''

for f in tb_ssl_list.find({'enable': True}):
    try:
        rst_time = ssl_monitor.ref_ssl_time(f['_id'])
        rst_day = int((rst_time - datetime.datetime.now()).total_seconds() / 86400)
        print('rst_day', rst_day)
        if rst_day <= ssl_min_day:
            print('报警')
            if total == 0:
                send_msg = '%s SSL证书还有%s天过期' % (f.get('host', ''), rst_day)
            total += 1
    except Exception as e:
        print(f['host'], e)

if total > 0:
    send_msg += ', 其他%s个域名也即将过期' % total
print(send_msg)
tools.send_server_jiang_msg(send_msg, send_msg)
