# -*- coding:utf-8 -*-
import os
import threading
import time

import tornado.options
import turbo.app
import turbo.register
from tornado.options import define, options

import setting

# uncomment this to init state managedocument.forms['form'].reset();r: store
# import store

turbo.register.register_app(
    setting.SERVER_NAME,
    setting.TURBO_APP_SETTING,
    setting.WEB_APPLICATION_SETTING,
    __file__,
    globals()
)

define("port", default=8861, type=int)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    turbo.app.start(options.port)
