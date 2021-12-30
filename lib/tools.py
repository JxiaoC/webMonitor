import datetime
import json
import os
import re
import random
import execjs
from urllib.parse import quote
from config import config
from bson import ObjectId
from cPython import cPython as cp
from helpers.web_monitor import setting
from turbo.core.exceptions import ResponseMsg

if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '__test__')):
    DEBUG = True
else:
    DEBUG = False
CHINAZ_JS_PATH = '%s/lib/chinaz.js' % config.PROJECT_DIR

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


def sec2hms(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if h >= 24 * 7:
        return "一周以前"
    if d > 0:
        return "%02d天%02d时%02d分%02d秒" % (d, h, m, s)
    if h > 0:
        return "%02d时%02d分%02d秒" % (h, m, s)
    elif m > 0:
        return "%02d分%02d秒" % (m, s)
    else:
        return "%02d秒" % s


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


def get_host_expire(host):
    context = execjs.compile(open(CHINAZ_JS_PATH, 'r').read())
    token = context.call("generateHostKey", host)
    url = 'http://whois.chinaz.com/getWhoisInfo.ashx'
    data = cp.post_for_request(url, _data={
        'token': token,
        'host': host,
        'isup': 'true',
        'ws': '',
    })
    if not data:
        raise ResponseMsg(-1, '获取失败')
    data = json.loads(data)
    if data.get('code', 0) != 1:
        raise ResponseMsg(-1, '获取失败')
    print(data.get('detail', ''))
    search_data = re.search('Expiration Time[:：].{0,1}(\d{4}-\d{2}-\d{2})', data.get('detail', ''))
    if not search_data:
        search_data = re.search('Registry Expiry Date[:：].{0,1}(\d{4}-\d{2}-\d{2})', data.get('detail', ''))
    if search_data:
        expire = datetime.datetime.strptime(search_data.group(1), '%Y-%m-%d')
        return expire
    else:
        raise ResponseMsg(-1, '无法获取到过期时间')


if __name__ == '__main__':
    # print(get_host_expire('xiaoc.cn'))
    print(sec2hms(97402))
    pass
