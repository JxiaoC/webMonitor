# -*- coding:utf-8 -*-
import requests
import turbo.log
from .base import BaseHandler
from helpers.web_monitor import server_monitor, server_monitor_real

logger = turbo.log.getLogger(__file__)


class ServerReportHandler(BaseHandler):
    def POST(self, type):
        self.route(type)

    def do_cpu(self):
        id = self.get_argument('id', '')
        value = self.get_argument('value', '')
        server_monitor.add_cpu_log(id, value)

    def do_load(self):
        id = self.get_argument('id', '')
        value = self.get_argument('value', '')
        server_monitor.add_load_log(id, value)

    def do_memory(self):
        id = self.get_argument('id', '')
        value = self.get_argument('value', '')
        total_value = self.get_argument('total_value', '')
        server_monitor.add_memory_log(id, value, total_value)

    def do_disk(self):
        id = self.get_argument('id', '')
        disk_name = self.get_argument('disk_name', '')
        mount_name = self.get_argument('mount_name', '')
        value = self.get_argument('value', '')
        total_value = self.get_argument('total_value', '')
        server_monitor.add_disk_log(id, disk_name, mount_name, value, total_value)

    def do_network(self):
        id = self.get_argument('id', '')
        time = self.get_argument('time', '')
        type = self.get_argument('type', '')
        value = self.get_argument('value', '')
        server_monitor.add_network_log(id, time, type, value)

    def do_all(self):
        data = self.get_argument('data')
        ip = self.request.remote_ip
        server_monitor.add_all(ip, data)
        pass


class ServerReportRealHandler(BaseHandler):
    def POST(self, type):
        self.route(type)

    def do_all(self):
        data = self.get_argument('data')
        ip = self.request.remote_ip
        server_monitor_real.add(ip, data)
        pass

