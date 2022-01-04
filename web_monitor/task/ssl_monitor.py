# -*- coding:utf-8 -*-
import datetime

import realpath
from helpers.web_monitor import setting, ssl_monitor
from models.web_monitor import model
from lib import tools

tb_ssl_list = model.SSLList()
ssl_min_day = int(setting.get().get('ssl_min_day', '1'))

for f in tb_ssl_list.find({'enable': True}):
    try:
        rst_time = ssl_monitor.ref_ssl_time(f['_id'])
        rst_day = int((rst_time - datetime.datetime.now()).total_seconds() / 86400)
        print('rst_day', rst_day)
        if rst_day <= ssl_min_day:
            print('报警')
            msg = '%s SSL证书还有%s天过期' % (f.get('host', ''), rst_day)
            tools.send_server_jiang_msg(msg, msg)
    except Exception as e:
        print(f['host'], e)