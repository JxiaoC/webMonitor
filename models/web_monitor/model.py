# -*- coding:utf-8 -*-
from bson import ObjectId
from datetime import datetime

from .base import *


class WebList(Model):
    """
    站点监控列表
        'name': 监控名称
        'atime': 添加时间
        'ltime': 最后一次执行监控的时间
        'warn_time': 报警时间
        'push_warn_time': 最后一次推送报警的时间
        'con_error_num': 连续错误次数
        'url': 监控url
        'enable': 启用状态
        'rate': 监控频率
        'allow_http_code': 允许返回的http状态码
        'header': 请求时发送的header
        'data': 请求时发送的post数据
        'method': 请求类型(GET/POST)
        'find_str': 查询返回内容, 不为空则表示启用该功能
        'find_str_type': 0=白名单模式, 1=黑名单模式, 白名单模式下, 如果查询未命中, 则失败; 黑名单模式下, 查询命中, 则失败
        'callback_url': 回调地址
    """
    name = 'web_list'

    field = {
        'name':                 (str,           None),
        'atime':                (datetime,      None),
        'ltime':                (datetime,      None),
        'warn_time':            (datetime,      None),
        'push_warn_time':       (datetime,      None),
        'con_error_num':        (int,           None),
        'url':                  (str,           None),
        'enable':               (bool,          None),
        'rate':                 (int,           None),
        'allow_http_code':      (list,         [200]),
        'header':               (str,           None),
        'data':                 (str,           None),
        'method':               (str,           None),
        'find_str':             (str,           None),
        'find_str_type':        (int,           None),
        'callback_url':         (str,           None),
    }


class SSLList(Model):
    """
    SSL监控列表
        'name': 监控名称
        'atime': 添加时间
        'ltime': 最后一次执行监控的时间
        'host': 监控域名
        'enable': 启用状态
        'rst_time': 过期时间
    """
    name = 'ssl_list'

    field = {
        'name':                 (str,           None),
        'atime':                (datetime,      None),
        'ltime':                (datetime,      None),
        'host':                 (str,           None),
        'enable':               (bool,          None),
        'rst_time':             (datetime,      None),
    }


class HostExpireList(Model):
    """
    域名过期时间监控列表
        'name': 监控名称
        'atime': 添加时间
        'ltime': 最后一次执行监控的时间
        'host': 监控域名
        'enable': 启用状态
        'rst_time': 过期时间
    """
    name = 'host_expire_list'

    field = {
        'name':                 (str,           None),
        'atime':                (datetime,      None),
        'ltime':                (datetime,      None),
        'host':                 (str,           None),
        'enable':               (bool,          None),
        'rst_time':             (datetime,      None),
    }


class WebLog(Model):
    """
    站点可用性日志
        'id': 站点id
        'atime': 记录时间
        'value': 延时(ms)
        'http_code': 返回http_code, 600=超时, 601=未知错误, 602=白名单报错, 603=黑名单报错
        'err_data': 发生错误时的错误信息
    """
    name = 'web_log'

    field = {
        'id':                   (ObjectId,      None),
        'atime':                (datetime,      None),
        'value':                (int,           None),
        'http_code':            (int,           None),
        'err_data':             (str,           None),
    }


class Setting(Model):
    """
    设置
    server_jiang_token: server酱token, 用于报警
    max_error_num: 连续超过N次错误即触发报警
    silence_time: 报警沉默时间(分钟)
    ssl_min_day: ssl证书有效期<=设置天数则触发报警
    host_expire_min_day: 域名有效期<=设置天数则触发报警
    """
    name = 'setting'

    field = {
        'server_jiang_token':                (str,           None),
        'max_error_num':                     (int,           None),
        'silence_time':                      (int,           None),
        'ssl_min_day':                       (int,           None),
        'host_expire_min_day':               (int,           None),
    }


class CallbackLog(Model):
    """
    回调日志
        'atime': 添加时间
        'status': 回调状态(success, fail)
        'callback_url': 回调url
        'rid': 所属监控id
        'enable': 当前启用状态(已完成或者最大错误次数超过3次时, 将会自动设置为false
        'complete': 是否已完成
        'error_num': 错误次数
    """
    name = 'callback_log'

    field = {
        'atime':               (datetime,           None),
        'status':              (str,                None),
        'callback_url':        (str,                None),
        'rid':                 (ObjectId,           None),
        'enable':             (bool,               True),
        'complete':            (bool,              False),
        'error_num':           (int,                   0),
    }


class ServerList(Model):
    """
    服务器监控列表
        'atime': 添加时间
        'utime': 修改时间(编辑/数据上报时更新)
    """
    name = 'server_list'

    field = {
        'atime':               (datetime,           None),
        'utime':               (datetime,           None),
        'name':                (str,                None),
        'ip':                  (str,                None),
        'desc':                (str,                None),
    }


class ServerCPULog(Model):
    """
    服务器监控CPU日志列表
        'atime': 添加时间
        'id': 服务器id
        'value': 当前占用cpu(百分比)
        'siblings': 核心数
    """
    name = 'server_cpu_log'

    field = {
        'atime':               (datetime,           None),
        'id':                  (ObjectId,           None),
        'value':               (float,                 0),
        'siblings':               (int,                   0),
    }


class ServerLoadLog(Model):
    """
    服务器监控负载日志列表
        'atime': 添加时间
        'id': 服务器id
        'value': 负载(1分钟,5分钟,15分钟)([1.5,1.0,0.8])
    """
    name = 'server_load_log'

    field = {
        'atime':               (datetime,           None),
        'id':                  (ObjectId,           None),
        'value':               (list,                 []),
    }


class ServerMemoryLog(Model):
    """
    服务器监控内存日志列表
        'atime': 添加时间
        'id': 服务器id
        'value': 当前占用内存(字节)
        'total_value': 总内存(字节)
    """
    name = 'server_memory_log'

    field = {
        'atime':               (datetime,           None),
        'id':                  (ObjectId,           None),
        'value':               (int,                   0),
        'total_value':         (int,                   0),
    }


class ServerDiskLog(Model):
    """
    服务器监控硬盘日志列表
        'atime': 添加时间
        'id': 服务器id
        'disk_name': 硬盘名称
        'mount_name': 硬盘挂载目录名称
        'value': 当前使用容量(字节)
        'total_value': 总容量(字节)
    """
    name = 'server_disk_log'

    field = {
        'atime':               (datetime,           None),
        'id':                  (ObjectId,           None),
        'disk_name':           (str,                  ''),
        'mount_name':          (str,                  ''),
        'value':               (int,                   0),
        'total_value':         (int,                   0),
    }


class ServerNetworkLog(Model):
    """
    服务器监控流量使用日志列表(只计算流出)
        'atime': 添加时间
        'id': 服务器id
        'time': 记录名称(2022011501, 年月日时)
        'value': 使用流量(字节)
    """
    name = 'server_network_log'

    field = {
        'atime':               (datetime,           None),
        'id':                  (ObjectId,           None),
        'time':                (int,                   0),
        'value':               (int,                   0),
    }


class SendServerJiangLog(Model):
    """
    发送server酱通知的日志文件
        'atime': 发送时间
        'text': 发送内容
        '发送状态': 0=成功, 1=失败
    """
    name = 'send_server_jiang_log'

    field = {
        'atime':               (datetime,           None),
        'text':                (str,                None),
        'status':              (int,                   0),
    }
