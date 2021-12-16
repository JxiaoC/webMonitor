import datetime
import json
import os
import random
from urllib.parse import quote

from bson import ObjectId
from cPython import cPython as cp
from helpers.web_monitor import setting
from turbo.core.exceptions import ResponseMsg

DEBUG = os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '__test__'))

common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key] = common_used_numerals_tmp[key]


def isint(a):
    try:
        int(a)
        return True
    except:
        return False


def chinese2digits(uchars_chinese):
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        val = common_used_numerals.get(uchars_chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return total


def send_server_jiang_msg(title, desp, server_jiang_token=None):
    if not server_jiang_token:
        server_jiang_token = setting.get().get('server_jiang_token', '')
    url = 'https://sctapi.ftqq.com/%s.send?title=%s&desp=%s' % (
        server_jiang_token,
        quote(title),
        quote(desp),
    )
    data = cp.get_html(url)
    if data is None:
        return False
    try:
        _ = json.loads(data)
        return _['code'] == 0
    except Exception as e:
        print('send_server_jiang_msg error,', e)
    return False


if __name__ == '__main__':
    # get_bilibili_userinfo()
    pass
