# -*- coding:utf-8 -*-
import time

import turbo.log

from helpers.web_monitor import http_monitor, setting, ssl_monitor
from lib import tools
from .base import BaseHandler

logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def get(self):
        self.render(
            'index.html',
        )


class HttpMonitorHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_list(self):
        page = int(self.get_argument('page', '1'))
        limit = int(self.get_argument('limit', '9999'))
        search_key = self.get_argument('search_key', '')
        search_value = self.get_argument('search_value', '')
        list, count = http_monitor.list(page, limit, search_key, search_value)
        self._data = {
            'list': list,
            'count': count,
        }

    def do_add(self):
        name = self.get_argument('name', '')
        url = self.get_argument('url', '')
        rate = int(self.get_argument('rate', '1'))
        self._data = http_monitor.add(name, url, rate)

    def do_remove(self):
        id = self.get_argument('id', '')
        self._data = http_monitor.remove(id)

    def do_edit(self):
        id = self.get_argument('id', '')
        key = self.get_argument('key', '')
        value = self.get_argument('value', '')
        self._data = http_monitor.edit(id, key, value)


class SSLHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_list(self):
        page = int(self.get_argument('page', '1'))
        limit = int(self.get_argument('limit', '9999'))
        search_key = self.get_argument('search_key', '')
        search_value = self.get_argument('search_value', '')
        list, count = ssl_monitor.list(page, limit, search_key, search_value)
        self._data = {
            'list': list,
            'count': count,
        }

    def do_add(self):
        name = self.get_argument('name', '')
        host = self.get_argument('host', '')
        self._data = ssl_monitor.add(name, host)

    def do_remove(self):
        id = self.get_argument('id', '')
        self._data = ssl_monitor.remove(id)

    def do_ref_all(self):
        self._data = ssl_monitor.ref_all()

    def do_edit(self):
        id = self.get_argument('id', '')
        key = self.get_argument('key', '')
        value = self.get_argument('value', '')
        self._data = ssl_monitor.edit(id, key, value)


class SettingHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_info(self):
        self._data = setting.get()

    def do_send(self):
        server_jiang_token = self.get_argument('server_jiang_token', '')
        self._data = setting.send_server_jiang_test(server_jiang_token)

    def do_save(self):
        server_jiang_token = self.get_argument('server_jiang_token', '')
        silence_time = self.get_argument('silence_time', '')
        max_error_num = self.get_argument('max_error_num', '')
        ssl_min_day = self.get_argument('ssl_min_day', '')
        self._data = setting.save(server_jiang_token, silence_time, max_error_num, ssl_min_day)

