import datetime
import re
import json

from bson import ObjectId

from models.web_monitor import model
from turbo.core.exceptions import ResponseMsg
from lib import tools

tb_setting = model.Setting()


def get():
    _ = tb_setting.find_one()
    if not _:
        _ = {
            'max_error_num': 3,
            'silence_time': 60,
            'ssl_min_day': 10,
            'server_jiang_token': '',
        }
        tb_setting.insert(_)
    return _


def send_server_jiang_test(server_jiang_token):
    if not tools.send_server_jiang_msg('Web监控', '当你收到这条消息时则表示配置成功!', server_jiang_token):
        raise ResponseMsg(-1, '发送失败, 请检查Token')


def save(server_jiang_token, silence_time, max_error_num, ssl_min_day):
    tb_setting.update({}, {'$set': {
        'server_jiang_token': server_jiang_token.strip(),
        'silence_time': int(silence_time),
        'max_error_num': int(max_error_num),
        'ssl_min_day': int(ssl_min_day),
    }})
