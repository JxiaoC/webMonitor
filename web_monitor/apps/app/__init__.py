# -*- coding:utf-8 -*-
from turbo import register

from . import api, god

register.register_group_urls('', [
    ('/', god.HomeHandler),
    ('/http_monitor/(add|list|remove|ref_episode|end|down|edit)', god.HttpMonitorHandler),
    ('/setting/(info|send|save)', god.SettingHandler),
])
