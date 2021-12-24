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
    """
    name = 'web_list'

    field = {
        'name':                 (str,           None),
        'atime':                (datetime,      None),
        'ltime':                (datetime,      None),
        'warn_time':            (datetime,      None),
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
    """
    name = 'web_log'

    field = {
        'id':                   (ObjectId,      None),
        'atime':                (datetime,      None),
        'value':                (int,           None),
        'http_code':            (int,           None),
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
