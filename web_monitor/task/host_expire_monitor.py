# -*- coding:utf-8 -*-
import datetime

import realpath
from helpers.web_monitor import setting, host_expire_monitor
from models.web_monitor import model
from lib import tools

tb_host_list = model.HostExpireList()
host_expire_min_day = int(setting.get().get('host_expire_min_day', '30'))
find_time = datetime.datetime.now() + datetime.timedelta(days=host_expire_min_day)

for f in tb_host_list.find({'enable': True, 'rst_time': {'$lte': find_time}}):
    rst_time = host_expire_monitor.ref_expire_time(f['_id'])
    rst_day = int((rst_time - datetime.datetime.now()).total_seconds() / 86400)
    print('rst_day', rst_day)
    if rst_day <= host_expire_min_day:
        print('报警')
        msg = '域名 %s 还有%s天过期, 请及时续费' % (f.get('host', ''), rst_day)
        tools.send_server_jiang_msg(msg, msg)