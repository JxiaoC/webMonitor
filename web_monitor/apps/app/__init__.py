# -*- coding:utf-8 -*-
from turbo import register

from . import api, god

register.register_group_urls('', [
    ('/', god.HomeHandler),
    ('/http_monitor/(add|list|remove|edit|edit_all)', god.HttpMonitorHandler),
    ('/ssl_monitor/(add|list|remove|edit|ref_all|ref)', god.SSLHandler),
    ('/expire_monitor/(add|list|remove|edit|ref)', god.HostExpireHandler),
    ('/setting/(info|send|save)', god.SettingHandler),
])
