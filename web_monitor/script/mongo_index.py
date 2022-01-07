# -*- coding:utf-8 -*-
import realpath
from models.web_monitor import model


_ = model.WebLog()
_.ensure_index([('id', -1), ('atime', -1)])
_.ensure_index([('id', -1), ('http_code', -1), ('atime', -1)])

_ = model.WebList()
_.ensure_index([('enable', -1), ('atime', -1)])

_ = model.SSLList()
_.ensure_index([('enable', -1), ('atime', -1)])

_ = model.HostExpireList()
_.ensure_index([('enable', -1), ('atime', -1)])

_ = model.CallbackLog()
_.ensure_index('enabled', -1)
_.ensure_index('rid', -1)
