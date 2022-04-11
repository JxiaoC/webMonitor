# -*- coding:utf-8 -*-
from turbo import register

from . import api, god

register.register_group_urls('', [
    ('/', god.HomeHandler),
    ('/http_monitor/list', god.HttpMonitorListHandler),
    ('/http_monitor/(add|remove|edit|edit_all|callback_test|test)', god.HttpMonitorHandler),
    ('/ssl_monitor/(add|list|remove|edit|ref_all|ref)', god.SSLHandler),
    ('/expire_monitor/(add|list|remove|edit|ref)', god.HostExpireHandler),
    ('/server_monitor/(add|list|remove|edit)', god.ServerHandler),
    ('/setting/(info|send|save)', god.SettingHandler),
    ('/server_report/(all)', api.ServerReportHandler),
])
