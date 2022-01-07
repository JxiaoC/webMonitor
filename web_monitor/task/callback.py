# 重新尝试发送回调地址
import datetime
import time

from bson import ObjectId
from cPython import cPython as cp
from models.web_monitor import model
from lib import tools
tb_callback_log = model.CallbackLog()


def new_callback(rid, callback_url, success):
    if not rid or not callback_url:
        return
    rid = ObjectId(rid)
    id = ObjectId()

    # 新建新的回调之前, 停止相同app之前的回调, 避免回调冲突
    tb_callback_log.update({'rid': rid}, {'$set': {
        'enable': False
    }}, multi=True)

    tb_callback_log.insert({
        '_id': id,
        'atime': datetime.datetime.now(),
        'callback_url': callback_url,
        'status': 'success' if success else 'fail',
        'rid': rid,
        'enable': True,
        'complete': False,
        'error_num': 0,
    })
    time.sleep(0.5)
    callback(id, success)


def callback(callback_id, success=True):
    callback_info = tb_callback_log.find_by_id(callback_id)
    if callback_info and not callback_info.get('enable', False):
        return

    callback_url = callback_info.get('callback_url', '')
    error_num = callback_info.get('error_num', '')

    callback_success = False
    try:
        html = cp.post_for_request(callback_url, _data={'status': 'success' if success else 'fail'})
        callback_success = html == 'ok'
    except Exception as e:
        print('callback 时发错误, %s' % e)
        pass

    if callback_success:
        tb_callback_log.update({'_id': ObjectId(callback_id)}, {'$set': {
            'enable': False,
            'complete': True,
        }})
    else:
        error_num += 1
        U = {
            'error_num': error_num
        }
        if error_num >= 3:
            U['enable'] = False
            U['complete'] = False
            tools.send_server_jiang_msg('回调失败', '[%s] 尝试回调 %s 时候发错误, 连续3次回调均失败' % (callback_id, callback_url))
        tb_callback_log.update({'_id': ObjectId(callback_id)}, {'$set': U})


for f in tb_callback_log.find({'enable': True}, {'_id': 1, 'status': 1}):
    status = f.get('status', '')
    callback(f['_id'], status == 'success')
